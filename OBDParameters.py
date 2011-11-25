class OBDParameters:
	SupportedPIDs = '0100'
	EngineLoad = '0104'
	EngineTemperature = '0105'
	RPM = '010C'
	VehicleSpeed = '010D'
	MAFAirFlow = '0110'
	ThrottlePosition = '0111'
	GetDiagnosticTrouleCodes = '03'
	ClearTroubleCodes = '04'

	Descriptions = {
		SupportedPIDs : {
			'bytes' : 4
		},
		
		EngineLoad : {
			'bytes' : 1,
			'index' : 4,
			'unit' : '%',
			'bounds' : {'min' : 0, 'max' : 100},
			'description' : 'Calculated engine load value'
		},
		
		EngineTemperature : {
			'bytes' : 1,
			'index' : 5,
			'unit' : 'C',
			'bounds' : {'min' : -40, 'max' : 215},
			'description' : 'Engine coolant temperature'
		},
		
		RPM : {
			'bytes' : 2,
			'index' : 12,
			'unit' : 'rpm',
			'bounds' : {'min' : 0, 'max' : 16383.75},
			'description' : 'Engine RPM'
		},
		
		VehicleSpeed : {
			'bytes' : 1,
			'index' : 13,
			'unit' : 'km/h',
			'bounds' : {'min' : 0, 'max' : 255},
			'description' : 'Vehicle speed'
		},
		
		MAFAirFlow : {
			'bytes' : 2,
			'index' : 16,
			'unit' : 'grams/sec',
			'bounds' : {'min' : 0, 'max' : 655.35},
			'description' : 'MAF air flow rate'
		},
		
		ThrottlePosition : {
			'bytes' : 1,
			'index' : 17,
			'unit' : '%',
			'bounds' : {'min' : 0, 'max' : 100},
			'description' : 'Throttle position'
		}
	}
