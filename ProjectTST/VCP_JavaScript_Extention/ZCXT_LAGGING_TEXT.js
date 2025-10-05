function ZCXT_LAGGING_TEXT(input) { 
    var log = sap.log();
    var jsonInput = JSON.parse(input);
    var cps_thickness, cps_width,cps_length,cps_dynamicDesc;
    var value1_p1 = 0.0;
    var value2_p1 = 0.0;
    var value3_p1 = 0.0;
    var value1_num = 0.0;
    var value2_num = 0.0;
    var value3_num = 0.0;
    
    try {
        cps_thickness = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'CXT_THICKNESS');
        cps_width = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'CXT_WIDTH');
        cps_length = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'CXT_LENGTH');
        cps_dynamicDesc = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'CXT_CUSTOM_TEXT');
    } catch (error) {
        // An exception can occur if no data has been provided
        log.error('Error: incomplete input data');
        throw new Error('Incomplete input');
    }
    
    if (typeof cps_thickness === 'undefined' || typeof cps_width === 'undefined' || typeof cps_length === 'undefined') { 
        // Exception handling: unexpected data input
		log.error('Error: incomplete input data - missing (one of) required input data');
        throw new Error('Incomplete input');
    }
    
    // CXT_THICKNESS
    const thicknessfeatures = cps_thickness.values;
    var thicknessVal = [...thicknessfeatures]

    switch (thicknessVal) {
        case 0.58:
          value1_p1 = 7;
          break;
        case 0.67:
          value1_p1 = 8;
          break;
        case 0.83:
          value1_p1 = 10;
          break;
        default:
          value1_p1 = thicknessVal * 12;
      }
    var value1_c = parseFloat(value1_p1.toFixed(2)).toString();

    const widthfeatures = cps_width.values;
    var thicknessVal = [...widthfeatures]
    value2_p1 = thicknessVal * 12;
    var value2_c = parseFloat(value2_p1.toFixed(2)).toString();

    const lengthfeatures = cps_length.values;
    var thicknessVal = [...lengthfeatures]
    value3_p1 = thicknessVal * 12;
    var value3_c = parseFloat(value3_p1.toFixed(2)).toString();

    // Concatenate the lagging text
    lagging_text = `${value1_c} in X ${value2_c} in X ${value3_c} in`;

    const features = cps_dynamicDesc.values;
    var descConds = [...features];
    log.debug('CXT_THICKNESS descConds cps_dynamicDesc------------>' + descConds);
    descConds.push(lagging_text);

    // // Prepare and return
    cps_dynamicDesc.values = descConds;
	
	// log.debug('Calculated descConds' + cps_dynamicDesc.values);
    
    return JSON.stringify({ type: 'vfun', vfunOutput: { result: true, fnArgs: [ cps_dynamicDesc ] } });
}