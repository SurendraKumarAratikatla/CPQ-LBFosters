function ZTW_TURNOUT_TEXT(input) { 
    var log = sap.log();
    var jsonInput = JSON.parse(input);
    var cps_TW_RAIL_SECTION, cps_TW_TR_ANGLE,cps_TW_FROG_STYLE, cps_TW_SW_STD_STYLE, cps_TW_TURNOUT_TEXT;
    try {
        cps_TW_RAIL_SECTION = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TW_RAIL_SECTION');
        cps_TW_TR_ANGLE = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TW_TR_ANGLE');
        cps_TW_FROG_STYLE = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TW_FROG_STYLE');
        cps_TW_SW_STD_STYLE = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TW_SW_STD_STYLE');

        cps_TW_TURNOUT_TEXT = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TW_TURNOUT_TEXT');

    } catch (error) {
        // An exception can occur if no data has been provided
        log.error('Error: incomplete input data');
        throw new Error('Incomplete input');
    }
    
    if (typeof cps_TW_RAIL_SECTION === 'undefined' || typeof cps_TW_TR_ANGLE === 'undefined' || typeof cps_TW_FROG_STYLE === 'undefined' || typeof cps_TW_SW_STD_STYLE === 'undefined' || typeof cps_TW_TURNOUT_TEXT === 'undefined') { 
        // Exception handling: unexpected data input
		log.error('Error: incomplete input data - missing (one of) required input data');
        throw new Error('Incomplete input');
    }
    
    // CXT_THICKNESS
    var value3_c,value4_c;
    const TW_RAIL_SECTIONfeatures = cps_TW_RAIL_SECTION.values;
    var value1_c = [...TW_RAIL_SECTIONfeatures]

    const TW_TR_ANGLEfeatures = cps_TW_TR_ANGLE.values;
    var value2_c = [...TW_TR_ANGLEfeatures]

    const TW_FROG_STYLEfeatures = cps_TW_FROG_STYLE.values;
    var value3_m = [...TW_FROG_STYLEfeatures]
    if(value3_m == "S"){
        value3_c = "SMSG";
    }
    else if(value3_m == "R"){
        value3_c = "RMBI";
    }
    else{
        value3_c = value3_m;
    }

    const TW_SW_STD_STYLEfeatures = cps_TW_SW_STD_STYLE.values;
    var value4_m = [...TW_SW_STD_STYLEfeatures]
    // if(value4_m == "NO"){
    //     value4_c = "";
    // }
    // else{
    //     value4_c = value4_m;
    // }


    // const LBF_PLUG_TEXTfeatures = cps_LBF_PLUG_TEXT.values;
    // var value8_c = [...LBF_PLUG_TEXTfeatures]



    // Concatenate the lagging text
    var value0_c = "Turnout -";
    if (value4_m == "NO"){
        var concat_text = `${value0_c} ${value1_c}RE #${value2_c} ${value3_c}`;
    }
    else{
        value4_c = value4_m;
        var concat_text = `${value0_c} ${value1_c}RE #${value2_c} ${value3_c} ${value4_c}`;
    }
    

    const features = cps_TW_TURNOUT_TEXT.values;
    var descConds = [...features];
    log.debug('ZTW_TURNOUT_TEXT: OUTPUT: cps_TW_TURNOUT_TEXT------------>' + descConds);
    descConds.push(concat_text);

    // // Prepare and return
    cps_TW_TURNOUT_TEXT.values = descConds;
	
	// log.debug('Calculated descConds' + cps_TW_TURNOUT_TEXT.values);
    
    return JSON.stringify({ type: 'vfun', vfunOutput: { result: true, fnArgs: [ cps_TW_TURNOUT_TEXT ] } });
}