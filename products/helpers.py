def unslugify(text):
	text = text.replace('-', ' ')
	text = text.title()
	return text

def cart_count(request):
	try:
		cart = request.session['cart']
		cart_len = len(cart)

	except:
		cart_len = 0

	return cart_len

def roundToTwoDecimalPlaces(number):
	return float("{:.2f}".format(number))

materials = ['medium', 'soft', 'firm', 'hard', 'dining chair', 'light', 'memory']

colours = ['blue', 'white', 'blue/recon', 'white/blue', 'floor', 'grey', 'black', 'custom']

pricing = {	'seating':	
						{	
							'sofa':	
									{	'back': 
											{	'medium': {	'blue': 0.011574074, 'white': 0.011574074, 'blue/recon': 0.011574074	},
												'soft': {	'blue': 0.010416667, 'white': 0.010416667, 'blue/recon': 0.010416667	},
												'firm': {	'blue': 0.012731481, 'white': 0.012731481, 'blue/recon': 0.012731481	},
											},
										'seat': 
											{	'medium': {	'blue': 0.010416667, 'white/blue': 0.010416667, 'blue/recon': 0.010416667	},
												'hard': {	'blue': 0.014467593, 'white/blue': 0.014467593, 'blue/recon': 0.014467593	},
												'firm': {	'blue': 0.012731481, 'white/blue': 0.012731481, 'blue/recon': 0.012731481	},
											}
									},

							'floor':
									{
										'floor': 
											{
												'medium': {	'floor': 0.010416667	},
												'firm': {	'floor': 0.012731481	},
												'hard': {	'floor': 0.016203704	}
											}
									},

							'dining-chair':
									{
										'dining-chair': 
											{
												'firm': {	'15x16x1': 3.5, '18x18x1': 4.2, '19x20x1': 5, '15x16x1.5': 5.25, '18x18x1.5': 6.75, '19x20x1.5': 7.5, '15x16x2': 7, '18x18x2': 8.4, '19x20x2': 10, '15x16x3': 10.5, '18x18x3': 13.5, '19x20x3': 15, '15x16x4': 14, '18x18x4': 16.8, '19x20x4': 20, 'custom': 0.012731481	},
												'hard': {	'15x16x1': 4.5, '18x18x1': 6, '19x20x1': 7, '15x16x1.5': 6.75, '18x18x1.5': 9, '19x20x1.5': 10, '15x16x2': 9, '18x18x2': 14, '19x20x2': 14, 'custom': 0.017361111	},
											}
									}
						},

			'sleeping':	
						{
							'mattress':
									{
										'mattress':
											{	'medium': {	'blue': 0.01099537, 'white': 0.01099537, 'white/blue': 0.01099537	},
												'soft': {	'blue': 0.009837963, 'white': 0.009837963, 'white/blue': 0.009837963	},
												'firm': {	'blue': 0.012731481, 'white': 0.012731481, 'white/blue': 0.012731481	},
											}
									},
							'topper':
									{
										'topper':
											{	'medium': {	'blue': 0.010416667, 'white': 0.010416667	},
												'firm': {	'blue': 0.012731481, 'white': 0.012731481	},
												'memory': {	'blue': 0.017361111, 'white': 0.017361111	}
											}
									}
						},

			'packaging': 
						{
							'packaging':
									{
										'packaging':
											{	'medium': {	'white': 0.010416667	},
												'hard': {	'black': 0.017361111, 'grey': 0.017361111	}
											}
									}
						},

			'sound-proofing': 
						{
							'sound-proofing':
									{
										'sound-proofing':
											{	'light': {	'white': 0.010416667	},
												'hard': {	'grey': 0.017361111		}
											}
									}
						},

			'craft': 
						{
							'craft':
									{
										'craft':
											{	'light': {	'white': 0.010416667	}
											}
									}
						}
		}