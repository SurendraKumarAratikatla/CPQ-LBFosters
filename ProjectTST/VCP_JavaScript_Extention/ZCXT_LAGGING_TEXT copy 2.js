function ZCXT_LAGGING_TEXT(input) { 
    var log = sap.log();
    var jsonInput = JSON.parse(input);

    var cps_drying_add_features, cps_varcond;
    
    try {
        cps_drying_add_features = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'CXT_THICKNESS');
        cps_varcond = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'CXT_WIDTH');
        cps_length = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'CXT_LENGTH');
        cps_dynamicDesc = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'CXT_CUSTOM_TEXT');
    } catch (error) {
        // An exception can occur if no fnArgs has been provided
        log.error('Error: incomplete input data - no fnArgs provided');
        throw new Error('Incomplete input');
    }
    
    if (typeof cps_drying_add_features === 'undefined' ||
        typeof cps_varcond === 'undefined') { 
        // Exception handling: unexpected fnArgs input
		log.error('Error: incomplete input data - missing (one of) CPS_DRYING_ADD_FEATURES/CPS_VARCOND');
        throw new Error('Incomplete input');
    }
    
    // Copy the values of CPS_DRYING_ADD_FEATURES to CPS_VARCOND
    const features = cps_drying_add_features.values;
    var varconds = [...features];
        
    // Special case: if 'SIF' and 'LIP', add 'SIFLIP_DISCOUNT'
    if (features.includes('SIF') && features.includes('LIP')) {
        varconds.push('SIFLIP_DISCOUNT');
    }
    
    // Special case: if > 3 features, add 'MANY_FEATURE_DISCOUNT'
    if (features.length > 3) {
        varconds.push('MANY_FEATURE_DISCOUNT');
    }
        
    // Prepare and return
    cps_varcond.values = varconds;
	
	log.debug('Calculated VARCONDS' + cps_varcond.values);
    
    return JSON.stringify({ type: 'vfun', vfunOutput: { result: true, fnArgs: [ cps_varcond ] } });
}