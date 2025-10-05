function ZWLS_FITTINGS_TEXT(input) { 
    var log = sap.log();
    var jsonInput = JSON.parse(input);
    var cpq_WLS_FITTING_TYPE, cpq_WLS_FITTING_DMNS,cpq_CTG_PIPE_TEXT;
    var value1m, value2m, value3m, value4m, value5m
    var value1_c,value2_c,value3_c,value4_c,value5_c

    
    try {
        cpq_WLS_FITTING_TYPE = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'WLS_FITTING_TYPE');
        cpq_WLS_FITTING_DMNS = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'WLS_FITTING_DMNS');

        cpq_CTG_PIPE_TEXT = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'CTG_PIPE_TEXT');
    } catch (error) {
        // An exception can occur if no data has been provided
        log.error('Error: incomplete input data');
        throw new Error('Incomplete input');
    }
    
    if (typeof cpq_WLS_FITTING_TYPE === 'undefined' || typeof cpq_WLS_FITTING_DMNS === 'undefined' || typeof cpq_CTG_PIPE_TEXT === 'undefined') { 
        // Exception handling: unexpected data input
		log.error('Error: incomplete input data - missing (one of) required input data');
        throw new Error('Incomplete input');
    }

    // WLS_FITTING_TYPE
    const wlsFitTypefeatures = cpq_WLS_FITTING_TYPE.values;
    var wlsFitTypeVal = [...wlsFitTypefeatures]
    var value1_c = wlsFitTypeVal

    var selectStatement = db.select()
        .from("CAWN")
        .build();
    var dbResult = db.execute(select);
    log.debug('ZWLS_FITTINGS_TEXT - dbResult 333333 ------------>' + dbResult);
    logTable(dbResult)
    // WLS_FITTING_DMNS
    const wlsFitDMNSfeatures = cpq_WLS_FITTING_DMNS.values;
    var wlsFitDMNSVal = [...wlsFitDMNSfeatures]
    var value2_c = wlsFitDMNSVal
    
    // Main conditions
    var Hie_sub_str_final = `${value1_c} ${value2_c}`

    // Concatenate the text
    Hie_text = `${Hie_sub_str_final}`;
    log.debug('ZWLS_FITTINGS_TEXT - Willis Coated Fittings 11111 ------------>' + Hie_text);
    const features = cpq_CTG_PIPE_TEXT.values;
    var descConds = [...features];
    log.debug('ZWLS_FITTINGS_TEXT - Willis Coated Fittings 22222 ------------>' + Hie_text);
    descConds.push(Hie_text);

    
    // // Prepare and return
    cpq_CTG_PIPE_TEXT.values = descConds;
    
    return JSON.stringify({ type: 'vfun', vfunOutput: { result: true, fnArgs: [ cpq_CTG_PIPE_TEXT ] } });
}