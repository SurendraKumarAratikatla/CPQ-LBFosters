function ZWLS_FITTINGS_PRD_HIERARCHY(input) { 
    var log = sap.log();
    var jsonInput = JSON.parse(input);
    var cpq_WLS_FITTING_TYPE, cpq_WLS_FITTING_DMNS,cpq_WLS_PIPE_WT_CONV,cpq_CTG_COATING_TYPE, cpq_WLS_IN_COATING_TYPE, cpq_CTG_PRODH;
    var value1m, value2m, value3m, value4m, value5m
    var value1_c,value2_c,value3_c,value4_c,value5_c

    
    try {
        cpq_WLS_FITTING_TYPE = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'WLS_FITTING_TYPE');
        cpq_WLS_FITTING_DMNS = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'WLS_FITTING_DMNS');
        cpq_WLS_PIPE_WT_CONV = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'WLS_PIPE_WT_CONV');
        cpq_CTG_COATING_TYPE = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'CTG_COATING_TYPE');
        cpq_WLS_IN_COATING_TYPE = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'WLS_IN_COATING_TYPE');

        cpq_CTG_PRODH = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'CTG_PRODH');
    } catch (error) {
        // An exception can occur if no data has been provided
        log.error('Error: incomplete input data');
        throw new Error('Incomplete input');
    }
    
    if (typeof cpq_WLS_FITTING_TYPE === 'undefined' || typeof cpq_WLS_FITTING_DMNS === 'undefined' || typeof cpq_WLS_PIPE_WT_CONV === 'undefined' || typeof cpq_CTG_COATING_TYPE === 'undefined' || typeof cpq_WLS_IN_COATING_TYPE === 'undefined') { 
        // Exception handling: unexpected data input
		log.error('Error: incomplete input data - missing (one of) required input data');
        throw new Error('Incomplete input');
    }
    
    // PREFIX VALUE
    var value0_c = "THD01"

    // WLS_FITTING_TYPE
    const wlsFitTypefeatures = cpq_WLS_FITTING_TYPE.values;
    var wlsFitTypeVal = [...wlsFitTypefeatures]
    var value1_c = wlsFitTypeVal

    // WLS_FITTING_DMNS
    const wlsFitDMNSfeatures = cpq_WLS_FITTING_DMNS.values;
    var wlsFitDMNSVal = [...wlsFitDMNSfeatures]
    
    if (Number.isInteger(Number(wlsFitDMNSVal)))
        {
            if(Number(wlsFitDMNSVal) < 8){
                value2m = 'OD1'
            }
            if(Number(wlsFitDMNSVal) < 18){
                value2m = 'OD2'
            }
            if(Number(wlsFitDMNSVal) < 24){
                value2m = 'OD3'
            }
            if(Number(wlsFitDMNSVal) < 30){
                value2m = 'OD4'
            }
            if(Number(wlsFitDMNSVal) < 36){
                value2m = 'OD5'
            }
            if(Number(wlsFitDMNSVal) < 48){
                value2m = 'OD6'
            }
            else{
                value2m = 'OD7'
            }
        }
    
    else{
        value2m = ''
    }

    var value2_c = (value2m).toString();

    // WLS_PIPE_WT_CONV
    const wlsPipeWtConvfeatures = cpq_WLS_PIPE_WT_CONV.values;
    var wlsPipeWtConvVal = [...wlsPipeWtConvfeatures]
    // var value2m = Math.floor(ppipeTypeVal * 1000);;
    // var value2_c = (value2m).toString();
    // var value7m;
    switch (String(wlsPipeWtConvVal)) {
        case 'A':
            value3m = 'WTA';
            break;
        case 'B':
            value3m = 'WTB';
            break;
        case 'C':
            value3m = 'WTC';
            break;
        case 'D':
            value3m = 'WTD';
            break;
        case 'E':
            value3m = "WTE";
            break;
        default:
            value3m = '';
    }
    var value3_c = (value3m).toString();

    // CTG_COATING_TYPE
    const ctgCoatingTypefeatures = cpq_CTG_COATING_TYPE.values;
    var ctgCoatingTypeVal = [...ctgCoatingTypefeatures]
    switch (String(ctgCoatingTypeVal)) {
        case 'FBE':
            value4m = 'LB027';
            break;
        case 'ARO':
            value4m = 'LB028';
            break;
        case 'LQD':
            value4m = 'LB029';
            break;
        default:
            value4m = '';
    }
    var value4_c = (value4m).toString();


    // WLS_IN_COATING_TYPE
    const wlsInCoatingfeatures = cpq_WLS_IN_COATING_TYPE.values;
    var wlsInCoatingVal = [...wlsInCoatingfeatures]
    switch (String(wlsInCoatingVal)) {
        case 'FBE':
            value5m = "LB027";
            break;
        case 'ARO':
            value5m = "LB028";
            break;
        case 'LQD':
            value5m = "LB029";
            break;
        default:
            value5m = '';
    }
    var value5_c = (value5m).toString();


    // Main conditions
    var Hie_sub_str_final = ''
    
    if(value2_c != "" || value2_c != null || value2_c != undefined){
        if(value5_c != "" && value4_c == ""){
            if(value1_c == "CAPS" || value1_c == "TEES STD"){
                Hie_sub_str_final = (value5_c + value1_c).padEnd(10, ' ') + value2_c + value3_c + 'ID'
            }
            else{
                Hie_sub_str_final = value5_c + value1_c + ' ' + value2_c + value3_c + 'ID'
            }
        }
        else if(value5_c == "" && value4_c != ""){
            if(value1_c == "CAPS" || value1_c == "TEES STD"){
                Hie_sub_str_final = (value4_c + value1_c).padEnd(10, ' ') + value2_c + value3_c + 'OD'
            }
            else{
                Hie_sub_str_final = value4_c + value1_c + ' ' + value2_c + value3_c + 'OD'
            }
        }

        else if(value5_c != "" && value4_c != ""){
            if(value1_c == "CAPS" || value1_c == "TEES STD"){
                Hie_sub_str_final = (value5_c + value1_c).padEnd(10, ' ') + value2_c + value3_c + 'BD'
            }
            else{
                Hie_sub_str_final = value5_c + value1_c + ' ' + value2_c + value3_c + 'BD'
            }
        }

    }
    else{
        if(value4_c != ""){
            Hie_sub_str_final = value4_c + value1_c
        }
        else{
            Hie_sub_str_final = value5_c + value1_c
        }

    }

    // Concatenate the text
    Hie_text = `${Hie_sub_str_final}`;

    const features = cpq_CTG_PRODH.values;
    var descConds = [...features];
    log.debug('ZWLS_FITTINGS_PRD_HIERARCHY Hie_text ------------>' + Hie_text);
    descConds.push(Hie_text);

    
    // // Prepare and return
    cpq_CTG_PRODH.values = descConds;
    
    return JSON.stringify({ type: 'vfun', vfunOutput: { result: true, fnArgs: [ cpq_CTG_PRODH ] } });
}