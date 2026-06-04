document.addEventListener("DOMContentLoaded", () => {
    // Initialize Lucide Icons
    lucide.createIcons();

    // Elements
    const churnForm = document.getElementById("churn-form");
    const monthlyChargesInput = document.getElementById("MonthlyCharges");
    const monthlyChargesVal = document.getElementById("monthly-charges-val");
    const phoneServiceInput = document.getElementById("PhoneService");
    const multipleLinesWrapper = document.getElementById("multiple-lines-wrapper");
    const multipleLinesInput = document.getElementById("MultipleLines");
    const btnReset = document.getElementById("btn-reset");
    const resultsCard = document.getElementById("results-card");
    const resultsPlaceholder = document.getElementById("results-placeholder");
    const resultsOutput = document.getElementById("results-output");
    const progressCircle = document.getElementById("progress-circle");
    const scorePercentage = document.getElementById("score-percentage");
    const scoreLabel = document.getElementById("score-label");
    const resultsBadge = document.getElementById("results-badge");
    const recommendationsList = document.getElementById("recommendations-list");
    const explainabilityFactorsContainer = document.getElementById("explainability-factors-container");

    // Circumference for SVG Progress Circle
    const radius = 50;
    const circumference = 2 * Math.PI * radius;
    if (progressCircle) {
        progressCircle.style.strokeDasharray = `${circumference} ${circumference}`;
        progressCircle.style.strokeDashoffset = circumference;
    }

    // Chart instances
    let explainChart = null;
    let churnDistChart = null;
    let chargesDistChart = null;
    let contractChurnChart = null;
    let retentionTrendsChart = null;

    // Monthly Charges Slider Text Update
    monthlyChargesInput.addEventListener("input", (e) => {
        monthlyChargesVal.textContent = `$${parseFloat(e.target.value).toFixed(2)}`;
    });

    // Phone Service dependencies: Auto-disable Multiple Lines if voice is off
    phoneServiceInput.addEventListener("change", (e) => {
        if (!e.target.checked) {
            multipleLinesInput.checked = false;
            multipleLinesWrapper.style.opacity = "0.4";
            multipleLinesInput.disabled = true;
        } else {
            multipleLinesWrapper.style.opacity = "1";
            multipleLinesInput.disabled = false;
        }
    });

    // Reset Form Action
    btnReset.addEventListener("click", () => {
        churnForm.reset();
        monthlyChargesVal.textContent = `$50.00`;
        multipleLinesWrapper.style.opacity = "1";
        multipleLinesInput.disabled = false;
        
        // Reset Results section
        resultsCard.classList.remove("churn-warning", "stay-success");
        resultsOutput.classList.add("hidden");
        resultsPlaceholder.classList.remove("hidden");
        explainabilityFactorsContainer.innerHTML = "";
        
        // Reset Progress ring
        if (progressCircle) {
            progressCircle.style.strokeDashoffset = circumference;
        }

        // Re-render Explainability chart to default
        renderExplainabilityChart([0,0,0,0,0,0,0,0,0]);
    });

    // Set Progress Bar Percentage on UI
    function setProgress(percent) {
        if (!progressCircle) return;
        const offset = circumference - (percent / 100) * circumference;
        progressCircle.style.strokeDashoffset = offset;
    }

    // Submit Prediction Form
    churnForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        // Change button state
        const submitBtn = document.getElementById("btn-predict");
        const originalBtnContent = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<i data-lucide="loader" class="animate-spin"></i> Calculating...`;
        lucide.createIcons();

        // Get Form Data
        const formData = {
            gender: document.getElementById("gender").value,
            SeniorCitizen: document.getElementById("SeniorCitizen").checked ? 1 : 0,
            PhoneService: document.getElementById("PhoneService").checked ? "Yes" : "No",
            MultipleLines: document.getElementById("PhoneService").checked 
                ? (document.getElementById("MultipleLines").checked ? "Yes" : "No")
                : "No phone service",
            StreamingTV: document.getElementById("StreamingTV").checked ? "Yes" : "No",
            StreamingMovies: document.getElementById("StreamingMovies").checked ? "Yes" : "No",
            PaperlessBilling: document.getElementById("PaperlessBilling").checked ? "Yes" : "No",
            MonthlyCharges: parseFloat(document.getElementById("MonthlyCharges").value),
            TotalCharges: parseFloat(document.getElementById("TotalCharges").value)
        };

        try {
            const response = await fetch("/api/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData)
            });

            if (!response.ok) throw new Error("API request failed");

            const result = await response.json();
            
            // Render Results Card
            resultsPlaceholder.classList.add("hidden");
            resultsOutput.classList.remove("hidden");
            resultsCard.classList.remove("churn-warning", "stay-success");

            if (result.churn) {
                // High risk of Churn
                resultsCard.classList.add("churn-warning");
                resultsBadge.textContent = "High Churn Risk";
                scoreLabel.textContent = "Churn Risk";
                scorePercentage.textContent = `${result.riskScore}%`;
                setProgress(result.riskScore);
            } else {
                // High Loyalty
                resultsCard.classList.add("stay-success");
                resultsBadge.textContent = "Loyalty Verified";
                scoreLabel.textContent = "Retention Score";
                scorePercentage.textContent = `${result.retentionScore}%`;
                setProgress(result.retentionScore);
            }

            // Recommendations List
            recommendationsList.innerHTML = "";
            result.recommendations.forEach(rec => {
                const li = document.createElement("li");
                li.innerHTML = `<strong>${rec.action}:</strong> ${rec.detail}`;
                recommendationsList.appendChild(li);
            });

            // Explainability drivers
            explainabilityFactorsContainer.innerHTML = "";
            result.factors.forEach(factor => {
                const badgeClass = factor.impact === "High Risk" ? "high-risk" : 
                                   factor.impact === "Medium Risk" ? "med-risk" : 
                                   factor.impact === "High Loyalty" ? "high-loyalty" : "low-risk";
                
                const item = document.createElement("div");
                item.className = "factor-item";
                item.innerHTML = `
                    <div class="factor-name-desc">
                        <span class="factor-name">${factor.name}</span>
                        <span class="factor-desc">${factor.description}</span>
                    </div>
                    <span class="factor-badge ${badgeClass}">${factor.impact}</span>
                `;
                explainabilityFactorsContainer.appendChild(item);
            });

            // Calculate feature importances relative weights customized to this prediction
            // Highlighting Monthly charges, etc.
            const importances = [2.47, 9.37, 0.92, 4.57, 4.68, 5.11, 6.85, 33.84, 32.20];
            const directionMap = importances.map((val, idx) => {
                // Assign visual highlight matching direction
                if (idx === 7) return formData.MonthlyCharges > 75 ? val : -val; // monthly charges
                if (idx === 8) return formData.TotalCharges > 1500 ? val : -val; // total charges
                if (idx === 1) return formData.SeniorCitizen === 1 ? val : -val; // senior citizen
                if (idx === 6) return formData.PaperlessBilling === "Yes" ? val : -val; // paperless
                return val;
            });
            renderExplainabilityChart(directionMap);

        } catch (error) {
            console.error("Error processing prediction:", error);
            alert("Failed to calculate prediction. Please verify inputs and check backend server logs.");
        } finally {
            // Restore button state
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnContent;
            lucide.createIcons();
        }
    });

    // Load Dashboard Analytics from Backend API
    async function loadDashboardAnalytics() {
        try {
            const response = await fetch("/api/analytics");
            if (!response.ok) throw new Error("Analytics API failed");
            const data = await response.json();

            // Populate KPIs
            document.getElementById("val-total").textContent = data.summary.totalCustomers.toLocaleString();
            document.getElementById("val-active").textContent = data.summary.activeCustomers.toLocaleString();
            document.getElementById("val-churn").textContent = `${data.summary.churnRate}%`;
            document.getElementById("val-accuracy").textContent = `${data.summary.modelAccuracy}%`;

            // Draw Charts
            drawChurnDistribution(data.churnDistribution);
            drawMonthlyCharges(data.monthlyCharges);
            drawContractChurn(data.contractChurn);
            drawRetentionTrends(data.retentionTrends);

            // Default blank explainability chart
            renderExplainabilityChart([0,0,0,0,0,0,0,0,0]);

        } catch (error) {
            console.error("Error loading analytics:", error);
        }
    }

    // Chart drawing functions using ApexCharts
    function drawChurnDistribution(distData) {
        const options = {
            series: distData.values,
            labels: distData.labels,
            chart: {
                type: 'donut',
                height: '100%',
                background: 'transparent'
            },
            colors: ['#22C55E', '#EF4444'],
            dataLabels: {
                enabled: false
            },
            stroke: {
                show: true,
                colors: ['#1E293B'],
                width: 2
            },
            legend: {
                position: 'bottom',
                fontSize: '12px',
                fontFamily: 'Inter, sans-serif',
                labels: {
                    colors: '#94A3B8'
                },
                markers: {
                    radius: 12
                }
            },
            tooltip: {
                theme: 'dark'
            },
            plotOptions: {
                pie: {
                    donut: {
                        size: '72%',
                        labels: {
                            show: true,
                            name: {
                                show: true,
                                color: '#94A3B8',
                                fontSize: '12px',
                                fontFamily: 'Inter'
                            },
                            value: {
                                show: true,
                                color: '#F8FAFC',
                                fontSize: '20px',
                                fontFamily: 'Poppins',
                                fontWeight: 600,
                                formatter: (val) => parseInt(val).toLocaleString()
                            },
                            total: {
                                show: true,
                                label: 'Customers',
                                color: '#94A3B8',
                                formatter: (w) => {
                                    return w.globals.seriesTotals.reduce((a, b) => a + b, 0).toLocaleString();
                                }
                            }
                        }
                    }
                }
            }
        };

        if (churnDistChart) churnDistChart.destroy();
        churnDistChart = new ApexCharts(document.querySelector("#chart-churn-distribution"), options);
        churnDistChart.render();
    }

    function drawMonthlyCharges(chargesData) {
        const options = {
            series: [
                { name: 'Retained', data: chargesData.retained },
                { name: 'Churned', data: chargesData.churned }
            ],
            chart: {
                type: 'area',
                height: '100%',
                background: 'transparent',
                toolbar: { show: false }
            },
            colors: ['#22C55E', '#EF4444'],
            dataLabels: { enabled: false },
            stroke: { curve: 'smooth', width: 2 },
            fill: {
                type: 'gradient',
                gradient: {
                    shadeIntensity: 1,
                    opacityFrom: 0.25,
                    opacityTo: 0.02,
                    stops: [0, 90, 100]
                }
            },
            grid: {
                borderColor: 'rgba(255, 255, 255, 0.05)',
                xaxis: { lines: { show: false } },
                yaxis: { lines: { show: true } }
            },
            xaxis: {
                categories: chargesData.labels,
                labels: {
                    style: { colors: '#94A3B8', fontFamily: 'Inter' }
                },
                axisBorder: { show: false },
                axisTicks: { show: false }
            },
            yaxis: {
                labels: {
                    style: { colors: '#94A3B8', fontFamily: 'Inter' }
                }
            },
            legend: {
                position: 'top',
                horizontalAlign: 'right',
                labels: { colors: '#94A3B8' }
            },
            tooltip: { theme: 'dark' }
        };

        if (chargesDistChart) chargesDistChart.destroy();
        chargesDistChart = new ApexCharts(document.querySelector("#chart-monthly-charges"), options);
        chargesDistChart.render();
    }

    // Interactive bar chart logic
    function drawContractChurn(contractData) {
        const options = {
            series: [
                { name: 'Retained', data: contractData.retained },
                { name: 'Churned', data: contractData.churned }
            ],
            chart: {
                type: 'bar',
                height: '100%',
                background: 'transparent',
                toolbar: { show: false }
            },
            colors: ['#22C55E', '#EF4444'],
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: '45%',
                    borderRadius: 4
                }
            },
            dataLabels: { enabled: false },
            stroke: { show: true, width: 2, colors: ['transparent'] },
            grid: {
                borderColor: 'rgba(255, 255, 255, 0.05)'
            },
            xaxis: {
                categories: contractData.categories,
                labels: {
                    style: { colors: '#94A3B8', fontFamily: 'Inter' }
                },
                axisBorder: { show: false }
            },
            yaxis: {
                labels: {
                    style: { colors: '#94A3B8', fontFamily: 'Inter' }
                }
            },
            legend: {
                position: 'top',
                horizontalAlign: 'right',
                labels: { colors: '#94A3B8' }
            },
            tooltip: { theme: 'dark' }
        };

        if (contractChurnChart) contractChurnChart.destroy();
        contractChurnChart = new ApexCharts(document.querySelector("#chart-contract-churn"), options);
        contractChurnChart.render();
    }

    function drawRetentionTrends(retentionData) {
        const options = {
            series: [{
                name: 'Retention Rate %',
                data: retentionData.retentionRates
            }],
            chart: {
                type: 'line',
                height: '100%',
                background: 'transparent',
                toolbar: { show: false }
            },
            colors: ['#3B82F6'],
            stroke: { curve: 'straight', width: 3 },
            markers: {
                size: 4,
                colors: ['#3B82F6'],
                strokeColors: '#1E293B',
                strokeWidth: 2
            },
            grid: {
                borderColor: 'rgba(255, 255, 255, 0.05)'
            },
            xaxis: {
                categories: retentionData.labels,
                labels: {
                    style: { colors: '#94A3B8', fontFamily: 'Inter' }
                },
                axisBorder: { show: false }
            },
            yaxis: {
                min: 0,
                max: 100,
                tickAmount: 5,
                labels: {
                    formatter: (val) => `${val}%`,
                    style: { colors: '#94A3B8', fontFamily: 'Inter' }
                }
            },
            tooltip: { theme: 'dark' }
        };

        if (retentionTrendsChart) retentionTrendsChart.destroy();
        retentionTrendsChart = new ApexCharts(document.querySelector("#chart-retention-trends"), options);
        retentionTrendsChart.render();
    }

    // Dynamic Explainability Chart (Specific to prediction values)
    function renderExplainabilityChart(dataValues) {
        const featureLabels = [
            "Gender", "Senior Citizen", "Phone Service", "Multiple Lines",
            "Streaming TV", "Streaming Movies", "Paperless Billing",
            "Monthly Charges", "Total Charges"
        ];

        const options = {
            series: [{
                name: 'Feature Impact Weight',
                data: dataValues.map(Math.abs)
            }],
            chart: {
                type: 'bar',
                height: 180,
                background: 'transparent',
                toolbar: { show: false }
            },
            colors: [function({ value, seriesIndex, dataPointIndex, w }) {
                // If it is Monthly Charges (index 7) or Total Charges (index 8)
                if (dataPointIndex === 7 || dataPointIndex === 8) {
                    return dataValues[dataPointIndex] >= 0 ? '#EF4444' : '#22C55E';
                }
                return '#3B82F6';
            }],
            plotOptions: {
                bar: {
                    borderRadius: 4,
                    horizontal: true,
                    barHeight: '70%',
                    distributed: true
                }
            },
            dataLabels: { enabled: false },
            grid: {
                borderColor: 'rgba(255, 255, 255, 0.05)',
                xaxis: { lines: { show: true } },
                yaxis: { lines: { show: false } }
            },
            xaxis: {
                categories: featureLabels,
                labels: {
                    style: { colors: '#94A3B8', fontFamily: 'Inter' }
                },
                axisBorder: { show: false }
            },
            yaxis: {
                categories: featureLabels,
                labels: {
                    style: { colors: '#94A3B8', fontFamily: 'Inter', fontSize: '10px' }
                }
            },
            legend: { show: false },
            tooltip: { theme: 'dark' }
        };

        if (explainChart) {
            explainChart.updateOptions(options);
        } else {
            explainChart = new ApexCharts(document.querySelector("#explainability-chart"), options);
            explainChart.render();
        }
    }

    // Run Initial Load
    loadDashboardAnalytics();
});