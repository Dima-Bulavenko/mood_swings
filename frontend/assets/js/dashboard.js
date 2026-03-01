const USER_ID_STORAGE_KEY = 'user_id';

if (!window.MoodSwingsClient) {
	throw new Error('MoodSwingsClient is not available. Include client.js before dashboard.js');
}

const moodClient = window.MoodSwingsClient.createClient();
const chartInstances = [];

function setStatus(elementId, message, isError = false) {
	const statusElement = document.getElementById(elementId);
	if (!statusElement) {
		return;
	}

	statusElement.textContent = message;
	statusElement.classList.toggle('error', isError);
}

function ensureChartJs() {
	if (!window.Chart) {
		throw new Error('Chart.js is not available. Include Chart.js before dashboard.js');
	}
}

function destroyExistingCharts() {
	while (chartInstances.length) {
		const chart = chartInstances.pop();
		chart.destroy();
	}
}

function toDisplayMoodName(moodName) {
	if (!moodName) {
		return moodName;
	}

	return String(moodName)
		.split(/[-_\s]+/)
		.map((part) => part.charAt(0).toUpperCase() + part.slice(1).toLowerCase())
		.join(' ');
}

function toShortDateLabel(isoDate) {
	const date = new Date(isoDate);
	if (Number.isNaN(date.getTime())) {
		return isoDate;
	}

	return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
}

async function ensureMoodSwingsUserId() {
	const storedUserId = localStorage.getItem(USER_ID_STORAGE_KEY);
	if (storedUserId) {
		return storedUserId;
	}

	const createdUser = await moodClient.createUser();
	if (!createdUser || !createdUser.id) {
		throw new Error('Failed to create user session.');
	}

	localStorage.setItem(USER_ID_STORAGE_KEY, createdUser.id);
	return createdUser.id;
}

function renderMoodFrequencyChart(data) {
	const canvas = document.getElementById('mood-frequency-chart');
	if (!canvas) {
		return;
	}

	if (!data.labels.length) {
		setStatus('mood-frequency-status', 'No mood data yet.');
		return;
	}

	setStatus('mood-frequency-status', '');
	const chart = new window.Chart(canvas, {
		type: 'bar',
		data: {
			labels: data.labels.map(toDisplayMoodName),
			datasets: [
				{
					label: 'Count',
					data: data.values,
					borderWidth: 1,
				},
			],
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
			plugins: {
				legend: {
					display: false,
				},
			},
			scales: {
				y: {
					beginAtZero: true,
					ticks: {
						precision: 0,
					},
				},
			},
		},
	});

	chartInstances.push(chart);
}

function renderWeeklyTrendChart(data) {
	const canvas = document.getElementById('weekly-trend-chart');
	if (!canvas) {
		return;
	}

	if (!data.labels.length) {
		setStatus('weekly-trend-status', 'No weekly trend data yet.');
		return;
	}

	setStatus('weekly-trend-status', '');

	const formattedMoods = data.moods.map(toDisplayMoodName);

	const chart = new window.Chart(canvas, {
		type: 'bar',
		plugins: [window.ChartDataLabels],
		data: {
			labels: data.labels,
			datasets: [
				{
					label: 'Top mood count',
					data: data.values,
					borderWidth: 1,
				},
			],
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
			plugins: {
				legend: { display: false },
				tooltip: { enabled: false },
				datalabels: {
					anchor: 'center',
					align: 'center',
					color: 'white',
					font: { weight: 'bold', size: 11 },
					formatter(_value, ctx) {
						return formattedMoods[ctx.dataIndex] ?? '';
					},
					display(ctx) {
						return ctx.dataset.data[ctx.dataIndex] > 0;
					},
				},
			},
			scales: {
				y: {
					beginAtZero: true,
					ticks: { precision: 0 },
				},
			},
		},
	});

	chartInstances.push(chart);
}

function renderTopHappyWordsChart(data) {
	const canvas = document.getElementById('happy-words-chart');
	if (!canvas) {
		return;
	}

	if (!data.labels.length) {
		setStatus('happy-words-status', 'No words data yet.');
		return;
	}

	setStatus('happy-words-status', '');
	const chart = new window.Chart(canvas, {
		type: 'bar',
		data: {
			labels: data.labels,
			datasets: [
				{
					label: 'Frequency',
					data: data.values,
					borderWidth: 1,
				},
			],
		},
		options: {
			indexAxis: 'y',
			responsive: true,
			maintainAspectRatio: false,
			plugins: {
				legend: {
					display: false,
				},
			},
			scales: {
				x: {
					beginAtZero: true,
					ticks: {
						precision: 0,
					},
				},
			},
		},
	});

	chartInstances.push(chart);
}

function renderUserHistoryChart(data) {
	const canvas = document.getElementById('user-history-chart');
	if (!canvas) {
		return;
	}

	const moodValues = data.moods.filter(Boolean).map(toDisplayMoodName);
	const uniqueMoodLevels = [...new Set(moodValues)];

	if (!data.labels.length) {
		setStatus('user-history-status', 'No history data yet.');
		return;
	}

	if (!uniqueMoodLevels.length) {
		setStatus('user-history-status', 'No moods logged in the last 7 days.');
	} else {
		setStatus('user-history-status', '');
	}

	const encodedMoodValues = data.moods.map((moodName) => {
		if (!moodName) {
			return null;
		}

		return uniqueMoodLevels.indexOf(toDisplayMoodName(moodName)) + 1;
	});

	const chart = new window.Chart(canvas, {
		type: 'line',
		data: {
			labels: data.labels.map(toShortDateLabel),
			datasets: [
				{
					label: 'Your mood',
					data: encodedMoodValues,
					spanGaps: false,
					tension: 0,
				},
			],
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
			plugins: {
				legend: {
					display: false,
				},
				tooltip: {
					callbacks: {
						label(context) {
							const moodName = data.moods[context.dataIndex];
							if (!moodName) {
								return 'No mood logged';
							}
							return `Mood: ${toDisplayMoodName(moodName)}`;
						},
					},
				},
			},
			scales: {
				y: {
					beginAtZero: true,
					ticks: {
						stepSize: 1,
						callback(value) {
							if (value <= 0 || value > uniqueMoodLevels.length) {
								return '';
							}

							return uniqueMoodLevels[value - 1];
						},
					},
					suggestedMax: uniqueMoodLevels.length + 1,
				},
			},
		},
	});

	chartInstances.push(chart);
}

async function loadDashboardData() {
	ensureChartJs();
	destroyExistingCharts();

	setStatus('mood-frequency-status', 'Loading...');
	setStatus('weekly-trend-status', 'Loading...');
	setStatus('user-history-status', 'Loading...');
	setStatus('happy-words-status', 'Loading...');

	try {
		const userId = await ensureMoodSwingsUserId();

		const [moodFrequencyResult, weeklyTrendResult, userHistoryResult, happyWordsResult] = await Promise.allSettled([
			moodClient.getMoodFrequency(),
			moodClient.getWeeklyTrend(),
			moodClient.getUserHistory(userId),
			moodClient.getTopHappyWords(),
		]);

		if (moodFrequencyResult.status === 'fulfilled') {
			renderMoodFrequencyChart(moodFrequencyResult.value);
		} else {
			setStatus('mood-frequency-status', 'Could not load mood frequency data.', true);
		}

		if (weeklyTrendResult.status === 'fulfilled') {
			renderWeeklyTrendChart(weeklyTrendResult.value);
		} else {
			setStatus('weekly-trend-status', 'Could not load weekly trend data.', true);
		}

		if (userHistoryResult.status === 'fulfilled') {
			renderUserHistoryChart(userHistoryResult.value);
		} else {
			setStatus('user-history-status', 'Could not load your mood history.', true);
		}

		if (happyWordsResult.status === 'fulfilled') {
			renderTopHappyWordsChart(happyWordsResult.value);
		} else {
			setStatus('happy-words-status', 'Could not load top happy words data.', true);
		}
	} catch (error) {
		setStatus('mood-frequency-status', 'Could not initialize dashboard.', true);
		setStatus('weekly-trend-status', 'Could not initialize dashboard.', true);
		setStatus('user-history-status', 'Could not initialize dashboard.', true);
		setStatus('happy-words-status', 'Could not initialize dashboard.', true);
		console.error('Unable to initialize dashboard:', error);
	}
}

loadDashboardData();
