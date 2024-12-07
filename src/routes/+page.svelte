<script>
	import { fade } from 'svelte/transition';
	import { writable } from 'svelte/store';

	const loading = writable(false);
	const error = writable('');
	// const results = writable(null);
	const results = writable({
		username: '',
		isFake: false,
		confidence: 0
	});
	let username = '';

	async function analyzeAccount() {
		if (!username.trim()) {
			error.set('Please enter a username');
			return;
		}

		loading.set(true);
		error.set('');
		// results.set(null);

		try {
			const response = await fetch('/analyze', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ username: username.trim() })
			});

			if (!response.ok) {
				const message = await response.text();
				throw new Error(`API request failed: ${message}`);
			}

			const data = await response.json();
			results.set({
				username: username.trim(),
				isFake: data.is_fake,
				confidence: parseFloat((data.fake_probability * 100).toFixed(1))
			});
		} catch (err) {
			console.error(err);
			error.set('An error occurred while analyzing the account');
		} finally {
			loading.set(false);
		}
	}
</script>

<div class="min-h-screen px-4 py-8">
	<div class="max-w-3xl mx-auto">
		<div class="text-center mb-12">
			<h1 class="text-4xl font-bold text-gray-900 mb-4">Instagram Account Analyzer</h1>
			<p class="text-gray-600">Check if an Instagram account is likely to be real or fake</p>
		</div>

		<div class="bg-white rounded-lg shadow-lg p-6 mb-8">
			<div class="flex flex-col md:flex-row gap-4">
				<div class="flex-grow">
					<input
						type="text"
						bind:value={username}
						placeholder="Enter Instagram username"
						class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
					/>
				</div>
				<button
					on:click={analyzeAccount}
					disabled={$loading}
					class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors flex items-center justify-center"
				>
					<span>Analyze</span>
					{#if $loading}
						<div
							class="ml-2 animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"
						></div>
					{/if}
				</button>
			</div>
			{#if $error}
				<div class="mt-2 text-red-500 text-sm">{$error}</div>
			{/if}
		</div>

		{#if $results}
			<div transition:fade class="bg-white rounded-lg shadow-lg p-6">
				<div class="flex items-center justify-between mb-4">
					<h3 class="text-xl font-semibold">Analysis Results for {username}:</h3>
					<span class="text-sm text-gray-500"></span>
				</div>
				<div class="flex items-center mb-4">
					<div
						class="w-12 h-12 rounded-full {$results.isFake
							? 'bg-red-100'
							: 'bg-green-100'} flex items-center justify-center"
					>
						<i
							class="bi {$results.isFake
								? 'bi-exclamation-triangle text-red-500'
								: 'bi-check-lg text-green-500'} text-xl"
						></i>
					</div>
					<div class="ml-4">
						<h4 class="font-semibold {$results.isFake ? 'text-red-500' : 'text-green-500'}">
							{$results.isFake ? 'Likely Fake Account' : 'Likely Real Account'}
						</h4>
						<p class="text-sm text-gray-600">Confidence: {$results.confidence}%</p>
					</div>
				</div>
				<div class="text-sm text-gray-600">
					<p>
						This analysis is based on available public data and patterns typically associated with {$results.isFake
							? 'fake'
							: 'authentic'} accounts.
					</p>
				</div>
			</div>
		{/if}

		<div class="mt-12 bg-white rounded-lg shadow-lg p-6">
			<h2 class="text-2xl font-semibold mb-4">About This Tool</h2>
			<p class="text-gray-600 mb-4">
				This tool uses advanced algorithms to analyze Instagram accounts and determine whether
				they're likely to be authentic or fake. The analysis is based on various factors including:
			</p>
			<ul class="list-disc list-inside text-gray-600 mb-4">
				<li>Account activity patterns</li>
				<li>Profile completeness</li>
				<li>Engagement metrics</li>
				<li>Content authenticity</li>
			</ul>
			<p class="text-gray-600">
				Please note that this is an estimation tool and results should be taken as indicative rather
				than definitive.
			</p>
		</div>

		<div class="mt-8 text-center">
			<p class="text-gray-600">
				Have feedback or questions?
				<a href="mailto:contact@example.com" class="text-blue-500 hover:text-blue-600">Contact us</a
				>
			</p>
		</div>
	</div>
</div>

<style>
	:global(body) {
		font-family: 'Inter', sans-serif;
		background-color: #f8fafc;
	}
</style>
