function ZTHR_PIPE_TEXT(input) { 
    var log = sap.log();
    var jsonInput = JSON.parse(input);
    var cpq_TH_PIPE_OD, cpq_TH_PIPE_WALL_THICKNESS,cpq_TH_PIPE_LENGTH,cpq_TH_PIPE_LENGTH_INCH, cpq_TH_PIPE_CAP_TYPE, cpq_TH_THREAD_TYPE,cpq_TH_PIPE_END,cpq_TH_PIPE_TYPE,cpq_TH_PIPE_SPECIAL,cpq_TH_PIPE_SOURCE,cpq_TH_OUTSIDE_OP,cpq_TH_PIPE_CAP_TYPE, cpq_TH_PIPE_TEXT;
    var value1m, value2m, value3m,value3m_1, value4m, value5m, value6m,value7m, value8m, value9m, value10m
    
    try {
        //INPUTS
        cpq_TH_PIPE_OD = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TH_PIPE_OD');
        cpq_TH_PIPE_WALL_THICKNESS = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TH_PIPE_WALL_THICKNESS');
        cpq_TH_PIPE_TYPE = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TH_PIPE_TYPE');
        cpq_TH_PIPE_SPECIAL = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TH_PIPE_SPECIAL');
        
        cpq_TH_PIPE_LENGTH = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TH_PIPE_LENGTH');
        cpq_TH_PIPE_LENGTH_INCH = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TH_PIPE_LENGTH_INCH');
        
        cpq_TH_PIPE_END = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TH_PIPE_END');
        cpq_TH_THREAD_TYPE = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TH_THREAD_TYPE');
        cpq_TH_PIPE_CAP_TYPE = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TH_PIPE_CAP_TYPE');
        cpq_TH_PIPE_SOURCE = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TH_PIPE_SOURCE');
        cpq_TH_OUTSIDE_OP = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TH_OUTSIDE_OP');

        
        //OUTPUT
        cpq_TH_PIPE_TEXT = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TH_PIPE_TEXT');
    } catch (error) {
        // An exception can occur if no data has been provided
        log.error('Error: incomplete input data');
        throw new Error('Incomplete input');
    }
    
    if (typeof cpq_TH_PIPE_OD === 'undefined' || typeof cpq_TH_PIPE_WALL_THICKNESS === 'undefined' || typeof cpq_TH_PIPE_TYPE === 'undefined' || typeof cpq_TH_PIPE_SPECIAL === 'undefined' || typeof cpq_TH_PIPE_LENGTH === 'undefined' || typeof cpq_TH_PIPE_LENGTH_INCH === 'undefined' ||  typeof cpq_TH_THREAD_TYPE === 'undefined' || typeof cpq_TH_PIPE_END === 'undefined') { 
        // Exception handling: unexpected data input
		log.error('Error: incomplete input data - missing (one of) required input data');
        throw new Error('Incomplete input');
    }
    
    // PREFIX VALUE
    var value0_c = "THD01"

    // TH_PIPE_OD
    const pipeOdfeatures = cpq_TH_PIPE_OD.values;
    var pipeOdVal = [...pipeOdfeatures]
    var value1m = Math.floor(parseFloat(pipeOdVal));
    var value1_c = (String(value1m)).toString();

    // TH_PIPE_WALL_THICKNESS
    const pipeWallThfeatures = cpq_TH_PIPE_WALL_THICKNESS.values;
    var pipeWallThVal = [...pipeWallThfeatures]
    var value2m = Math.floor(pipeWallThVal * 1000);;
    if (String(value2m).slice(1) == '00'){
        var value2_c = '.'+(String(value2m).slice(0,2)).toString();
    }
    else{
        var value2_c = '.'+(String(value2m).slice(0,3)).toString();
    }

    // TH_PIPE_TYPE
    const pipeTypefeatures = cpq_TH_PIPE_TYPE.values;
    var ppipeTypeVal = [...pipeTypefeatures]
    // var value2m = Math.floor(ppipeTypeVal * 1000);;
    // var value2_c = (value2m).toString();
    // var value7m;
    switch (String(ppipeTypeVal)) {
        case 'SS 304':
            value7m = '304SS';
            if(value8m == 'S'){
                value8m = 'SMLS';
            }
            else{
                value8m = '';
            }
            break;
        case 'SS 316':
            value7m = '316SS';
            if(value8m == 'S'){
                value8m = 'SMLS';
            }
            else{
                value8m = '';
            }
            break;
        case 'A106B-SLS':
            value7m = 'SMLS';
            value8m = '';
            break;
        case 'ERW':
            value7m = '';
            value8m = '';
            break;
        case 'STU':
            value7m = "STU";
            value8m = '';
            break;
        default:
            value7m = ppipeTypeVal;
    }
    var value7_c = (value7m).toString();
    var value8_c = (value8m).toString(); //TH_PIPE_SPECIAL
    

    // TH_PIPE_LENGTH
    const pipeLenfeatures = cpq_TH_PIPE_LENGTH.values;
    var pipeLenVal = [...pipeLenfeatures]
    var value3_c,value3_c_1;
    if(parseFloat(pipeLenVal) != 0.0){
        value3m = pipeLenVal
        value3_c = (String(value3m)+ '0' + "'").toString();
    }

    // TH_PIPE_LENGTH
    const pipeLenInchfeatures = cpq_TH_PIPE_LENGTH_INCH.values;
    var pipeLenInchVal = [...pipeLenInchfeatures]
    if (pipeLenInchVal != 0.0){
        value3m_1 = pipeLenInchVal
        value3_c_1 = (String(value3m_1) + '0' + '"').toString();
    }
    
    // TH_THREAD_TYPE
    const threadTypefeatures = cpq_TH_THREAD_TYPE.values;
    var threadTypeVal = [...threadTypefeatures]
    // var value2m = Math.floor(ppipeTypeVal * 1000);;
    // var value2_c = (value2m).toString();
    // var value5m
    //var value5_c = (value5m).toString();


    // TH_PIPE_CAP_TYPE
    const pipeCapTypefeatures = cpq_TH_PIPE_CAP_TYPE.values;
    var pipeCapTypeVal = [...pipeCapTypefeatures]
    value4m = String(pipeCapTypeVal)


    // TH_PIPE_END
    const pipeEndfeatures = cpq_TH_PIPE_END.values;
    var pipeEndVal = [...pipeEndfeatures]
    // var value2m = Math.floor(pipeEndVal * 1000);;
    // var value2_c = (value2m).toString();
    // var value7m;
    
    if (String(pipeEndVal) == 'T&C'){
        value6m = 'TC';
        switch (String(value4m)) {
            case '8RDS':
                value4m = 'API 8RD STC';
                break;
            case '8RDL':
                value4m = 'API 8RD LTC';
                break;
            case '8VLP':
                value4m = 'API LP';
                break;
            case 'JS-D':
                value4m = 'JS DOM';
                break;
            case 'TS-D':
                value4m = 'TS DOM';
                break;
            case 'JNAB':
                value4m = 'J NAB';
                break;
            case 'TNAB':
                value4m = 'T NAB';
                break;
                    
            default:
                value4m = String(pipeCapTypeVal);
        };
    }
    else{
        value4m = ''
    }

    //

    if (String(pipeEndVal) == 'TBE' || String(pipeEndVal) == 'TOE' || (String(value6m) == 'TC')){
        switch (String(threadTypeVal)) {
            case 'APILP':
                value5m = 'API LP';
                break;
            case '8RDS':
                value5m = 'API 8RD SH';
                break;
            case '8RDL':
                value5m = 'API 8RD LG';
                break;
            case 'BUTT':
                value5m = 'BTC';
                break;
            case 'TXW':
                value5m = 'T X W';
                break;
            case 'TX8RDS':
                value5m = 'T X 8RD SH';
                break;
            case 'TX8RDL':
                value5m = 'T X 8RD LG';
                break;
                    
            default:
                value5m = String(threadTypeVal);
        };
    }
    else{
        value6m = pipeEndVal
        value5m = ''
    }

    var value5_c = (value5m).toString();
    var value6_c = (value6m).toString();
    var value4_c = (value4m).toString();


    // TH_PIPE_SOURCE Value 9 
    const pipeSourcefeatures = cpq_TH_PIPE_SOURCE.values;
    var pipeSourceVal = [...pipeSourcefeatures]
    if (String(pipeSourceVal) == 'D'){
        value9m = 'DOM'
    }
    else{
        value9m = ''
    }
    var value9_c = (value9m).toString();


    // TH_OUTSIDE_OP value 10
    const thOutideOpfeatures = cpq_TH_OUTSIDE_OP.values;
    var thOutideOpVal = [...thOutideOpfeatures]
    if (String(thOutideOpVal) == 'C'){
        value10m = 'CTD'
    }
    else if(String(thOutideOpVal) == 'G'){
        value10m = 'GALV'
    }
    else if(String(thOutideOpVal) == 'S'){
        value10m = 'SB'
    }
    else{
        value10m = ''
    }
    var value10_c = (value10m).toString();


    
    // Main conditions
    var pipe_text_concat

    if(parseFloat(value3m) > 0.0){
        pipe_text_concat = `${value1_c} ${value2_c} ${value3_c}` //String(value1_c) + ' ' +String(value2_c) +  ' '+ value3_c_1 
    }
    else if(parseFloat(value3m_1) > 0.0){
        pipe_text_concat = `${value1_c} ${value2_c} ${value3_c_1}` // String(value1_c) + ' ' +String(value2_c) +  ' '+ value3_c;
    }

    if(value5_c != 'NA' && value5_c != ''){
        pipe_text_concat = `${pipe_text_concat} ${value5_c}` // pipe_text_concat + ' ' + value5_c
    }

    if(value4_c != 'NA' && value4_c != ''){
        pipe_text_concat = `${pipe_text_concat} ${value4_c}` // pipe_text_concat + ' ' + value4_c
    }

    if(value6_c != 'NA' && value6_c != ''){
        pipe_text_concat = `${pipe_text_concat} ${value6_c}` // pipe_text_concat + ' ' + value6_c
    }

    if(value7_c != 'NA' && value7_c != ''){
        pipe_text_concat = `${pipe_text_concat} ${value7_c}` // pipe_text_concat + ' ' + value7_c
    }

    if(value8_c != 'NA' && value8_c != ''){
        pipe_text_concat = `${pipe_text_concat} ${value8_c}` // pipe_text_concat + ' ' + value8_c
    }

    if(value9_c != 'NA' && value9_c != ''){
        pipe_text_concat = `${pipe_text_concat} ${value9_c}` // pipe_text_concat + ' ' + value9_c
    }
    
    if(value10_c != 'NA' && value10_c != ''){
        pipe_text_concat = `${pipe_text_concat} ${value10_c}` // pipe_text_concat + ' ' + value10_c
    }
    
    // Concatenate the text
    Pipe_text = `${pipe_text_concat}`;

    const features = cpq_TH_PIPE_TEXT.values;
    var descConds = [...features];
    log.debug('cpq_TH_PIPE_TEXT value3_c------------>' + pipeLenVal);
    log.debug('cpq_TH_PIPE_TEXT value3_c_1------------>' + pipeLenInchVal);
    descConds.push(Pipe_text);

    
    // // Prepare and return
    cpq_TH_PIPE_TEXT.values = descConds;
    
    return JSON.stringify({ type: 'vfun', vfunOutput: { result: true, fnArgs: [ cpq_TH_PIPE_TEXT ] } });
}