function ZCTG_PIPE_TEXT(input) { 
    var log = sap.log();
    var jsonInput = JSON.parse(input);
    var cpq_CTG_PIPE_OD, cpq_CTG_PIPE_WALL_THICKNESS,cpq_CTG_COATING_TYPE,cpq_CTG_COATING_1_MIL, cpq_CTG_COATING_2_MIL, cpq_CTG_PIPE_TEXT;
    var value5m, value6m, value7m

    
    try {
        cpq_CTG_PIPE_OD = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'CTG_PIPE_OD');
        cpq_CTG_PIPE_WALL_THICKNESS = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'CTG_PIPE_WALL_THICKNESS');
        cpq_CTG_COATING_TYPE = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'CTG_COATING_TYPE');
        cpq_CTG_COATING_1_MIL = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'CTG_COATING_1_MIL');
        cpq_CTG_COATING_2_MIL = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'CTG_COATING_2_MIL');

        cpq_CTG_PIPE_TEXT = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'CTG_PIPE_TEXT');
    } catch (error) {
        // An exception can occur if no data has been provided
        log.error('Error: incomplete input data');
        throw new Error('Incomplete input');
    }
    
    if (typeof cpq_CTG_PIPE_OD === 'undefined' || typeof cpq_CTG_PIPE_WALL_THICKNESS === 'undefined' || typeof cpq_CTG_COATING_TYPE === 'undefined' || typeof cpq_CTG_COATING_1_MIL === 'undefined' || typeof cpq_CTG_COATING_2_MIL === 'undefined') { 
        // Exception handling: unexpected data input
		log.error('Error: incomplete input data - missing (one of) required input data');
        throw new Error('Incomplete input');
    }
    

    // CTG_PIPE_OD
    const CTGpipeOdfeatures = cpq_CTG_PIPE_OD.values;
    var CTGpipeOdVal = [...CTGpipeOdfeatures]
    var value1m = Math.floor(parseFloat(CTGpipeOdVal));
    var value1_c = (String(value1m)).toString();

    // CTG_PIPE_WALL_THICKNESS
    const CTGpipeWallThfeatures = cpq_CTG_PIPE_WALL_THICKNESS.values;
    var CTGpipeWallThVal = [...CTGpipeWallThfeatures]
    //var value2m = String(CTGpipeWallThVal);
    var value2_c = (CTGpipeWallThVal).toString();

    // CTG_COATING_TYPE
    const CTGCotTypefeatures = cpq_CTG_COATING_TYPE.values;
    var CTGCotTypeVal = [...CTGCotTypefeatures]
    var value3_c = (CTGCotTypeVal).toString()


    // CTG_COATING_TYPE
    const CTGCotType1features = cpq_CTG_COATING_1_MIL.values;
    var CTGCotType1Val = [...CTGCotType1features]
    var value4_c = (CTGCotType1Val).toString().split('.')[0]

    // CTG_COATING_TYPE
    const CTGCotType2features = cpq_CTG_COATING_2_MIL.values;
    var CTGCotType2Val = [...CTGCotType2features]
    var value5_c = (CTGCotType2Val).toString().split(".")[0]

    // Main condition
    var pipe_text_concat;
    if (value3_c == 'FBE'){
        pipe_text_concat = value1_c + ' X ' + value2_c + ' ' +value3_c + ' Mil ' + value4_c
    }
    else{
        pipe_text_concat = value1_c + ' X ' + value2_c + ' ' +value3_c + ' Mil ' + value4_c + ' ' + '/' + ' ' + value5_c
    }



    // Concatenate the text
    var ctg_pipe_text = `${pipe_text_concat}`;

    const features = cpq_CTG_PIPE_TEXT.values;
    var descConds = [...features];
    log.debug('ctg_pipe_text------------>' + ctg_pipe_text);
    descConds.push(ctg_pipe_text);

    
    // // Prepare and return
    cpq_CTG_PIPE_TEXT.values = descConds;
    
    return JSON.stringify({ type: 'vfun', vfunOutput: { result: true, fnArgs: [ cpq_CTG_PIPE_TEXT ] } });
}