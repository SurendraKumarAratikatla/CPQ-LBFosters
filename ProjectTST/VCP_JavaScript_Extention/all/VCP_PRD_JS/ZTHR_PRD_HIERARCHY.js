function ZTHR_PRD_HIERARCHY(input) { 
    var log = sap.log();
    var jsonInput = JSON.parse(input);
    var cpq_TH_PIPE_OD, cpq_TH_PIPE_WALL_THICKNESS,cpq_TH_PIPE_TYPE,cpq_TH_THREAD_TYPE, cpq_TH_PIPE_END, cpq_H_PRODH;
    var value5m, value6m, value7m
    
    try {
        //Input fields
        cpq_TH_PIPE_OD = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TH_PIPE_OD');
        cpq_TH_PIPE_WALL_THICKNESS = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TH_PIPE_WALL_THICKNESS');
        cpq_TH_PIPE_TYPE = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TH_PIPE_TYPE');
        cpq_TH_THREAD_TYPE = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TH_THREAD_TYPE');
        cpq_TH_PIPE_END = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TH_PIPE_END');

        //output field
        cpq_H_PRODH = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'TH_PRODH');
    } catch (error) {
        // An exception can occur if no data has been provided
        log.error('Error: incomplete input data');
        throw new Error('Incomplete input');
    }
    
    // if (typeof cpq_TH_PIPE_OD === 'undefined' || typeof cpq_TH_PIPE_WALL_THICKNESS === 'undefined' || typeof cpq_TH_PIPE_TYPE === 'undefined' || typeof cpq_TH_THREAD_TYPE === 'undefined' || typeof cpq_TH_PIPE_END === 'undefined') { 
    //     // Exception handling: unexpected data input
	// 	log.error('Error: incomplete input data - missing (one of) required input data');
    //     throw new Error('Incomplete input');
    // }
    
    // PREFIX VALUE
    var value0_c = "THD01"

    // TH_PIPE_OD
    const pipeOdfeatures = cpq_TH_PIPE_OD.values;
    var pipeOdVal = [...pipeOdfeatures]
    var value1m = Math.floor(parseFloat(pipeOdVal));
    var value1_c = (value1m < 10 ? "0" + String(value1m):value1m).toString();

    // TH_PIPE_WALL_THICKNESS
    const pipeWallThfeatures = cpq_TH_PIPE_WALL_THICKNESS.values;
    var pipeWallThVal = [...pipeWallThfeatures]
    var value2m = Math.floor(pipeWallThVal * 1000);
    var value2_c = (value2m).toString();

    // TH_PIPE_TYPE
    const pipeTypefeatures = cpq_TH_PIPE_TYPE.values;
    var ppipeTypeVal = [...pipeTypefeatures]
    // var value2m = Math.floor(ppipeTypeVal * 1000);;
    // var value2_c = (value2m).toString();
    // var value7m;
    switch (String(ppipeTypeVal)) {
        case 'SS 304':
            value7m = 'S304';
            break;
        case 'SS 316':
            value7m = 'S316';
            break;
        case 'A106B-SLS':
            value7m = 'SMLS';
            break;
        case 'ERW':
            value7m = 'ERW';
            break;
        case 'STU':
            value7m = "STU";
            break;
        default:
            value7m = '';
    }
    var value7_c = (value7m).toString();

    // TH_THREAD_TYPE
    const threadTypefeatures = cpq_TH_THREAD_TYPE.values;
    var threadTypeVal = [...threadTypefeatures]
    // var value2m = Math.floor(ppipeTypeVal * 1000);;
    // var value2_c = (value2m).toString();
    // var value5m
    switch (String(threadTypeVal)) {
        case 'APILP':
            value5m = 'A';
            break;
        case '8RDS':
            value5m = 'R';
            break;
        case '8RDL':
            value5m = 'R';
            break;
        case 'BUTT':
            value5m = 'B';
            break;
        case 'TXW':
            value5m = "T";
            break;
        case 'TX8RDS':
            value5m = "T";
            break;
        case 'TX8RDL':
            value5m = "T";
            break;
        case 'LB':
            value5m = "L";
            break;
        case 'NA':
            value5m = "NA";
            break;
        default:
            value5m = 'NA';
    }
    var value5_c = (value5m).toString();


    // TH_PIPE_END
    const pipeEndfeatures = cpq_TH_PIPE_END.values;
    var pipeEndVal = [...pipeEndfeatures]
    // var value2m = Math.floor(pipeEndVal * 1000);;
    // var value2_c = (value2m).toString();
    // var value7m;
    switch (String(pipeEndVal)) {
        case 'FLXT':
            value6m = 'FLG';
            value5m = "";
            break;
        case 'FLXW':
            value6m = 'FLG';
            value5m = "";
            break;
        default:
            value6m = pipeEndVal;
    }
    var value6_c = (value6m).toString();

    // Main conditions
    var Hie_sub_str_final = ''
    if(value7_c == 'ERW'){
        var Hie_sub_text1 = `${value1_c}${value2_c}${value7_c}`
        if(value5_c != 'NA'){
            var Hie_sub_text2 = ' '+`${value5_c}${value6_c}`
            Hie_sub_str_final = Hie_sub_text1 + Hie_sub_text2
        }
        else{
            var Hie_sub_text2 = Hie_sub_text1.padEnd(10, ' ') +`${value6_c}`;
            Hie_sub_str_final = Hie_sub_text2
        }
        
    }
    else{
        
        if(value5_c != 'NA'){
            Hie_sub_str_final = `${value1_c}${value2_c}${value7_c}${value5_c}${value6_c}`
            // var Hie_sub_text2 = `${value5_c} ${value6_c}`
        }
        else{
            var Hie_sub_text1 = `${value1_c}${value2_c}${value7_c}`
            var Hie_sub_text2 = ' ' +`${value6_c}`;
            Hie_sub_str_final = Hie_sub_text1 + Hie_sub_text2
        }
        
    }

    // Concatenate the text
    Hie_text = `${value0_c}${Hie_sub_str_final}`;

    const features = cpq_H_PRODH.values;
    var descConds = [...features];
    log.debug('ppipeTypeVal------------>' + ppipeTypeVal);
    descConds.push(Hie_text);

    // // Prepare and return
    cpq_H_PRODH.values = descConds;
    
    // converting the javascript object to stirng and returning
    return JSON.stringify({ type: 'vfun', vfunOutput: { result: true, fnArgs: [ cpq_H_PRODH ] } });
}