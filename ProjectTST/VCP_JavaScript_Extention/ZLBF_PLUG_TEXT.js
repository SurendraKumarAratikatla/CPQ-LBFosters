function ZLBF_PLUG_TEXT(input) { 
    var log = sap.log();
    var jsonInput = JSON.parse(input);
    var cps_RAIL_SECTION, cps_ARP_CUST_SPEC,cps_ARP_DRILL_PATTERN, cps_ARP_PLUG_TYPE, cps_OA_LENGTH_STRING,cps_ARP_FASTENER_TYPE, cps_DESC_UPDATE,cps_LBF_PLUG_TEXT
    try {
        cps_RAIL_SECTION = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'RAIL_SECTION');
        cps_ARP_CUST_SPEC = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'ARP_CUST_SPEC');
        cps_ARP_DRILL_PATTERN = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'ARP_DRILL_PATTERN');
        cps_ARP_PLUG_TYPE = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'ARP_PLUG_TYPE');
        cps_OA_LENGTH_STRING = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'OA_LENGTH_STRING');
        cps_ARP_FASTENER_TYPE = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'ARP_FASTENER_TYPE');
        cps_DESC_UPDATE = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'DESC_UPDATE');
        cps_LBF_PLUG_TEXT = jsonInput.vfunInput.fnArgs.find(({ id }) => id === 'LBF_PLUG_TEXT');

    } catch (error) {
        // An exception can occur if no data has been provided
        log.error('Error: incomplete input data');
        throw new Error('Incomplete input');
    }
    
    if (typeof cps_RAIL_SECTION === 'undefined' || typeof cps_ARP_CUST_SPEC === 'undefined' || typeof cps_ARP_DRILL_PATTERN === 'undefined' || typeof cps_ARP_PLUG_TYPE === 'undefined' || typeof cps_OA_LENGTH_STRING === 'undefined' || typeof cps_ARP_FASTENER_TYPE === 'undefined' || typeof cps_DESC_UPDATE === 'undefined' || typeof cps_LBF_PLUG_TEXT === 'undefined') { 
        // Exception handling: unexpected data input
		log.error('Error: incomplete input data - missing (one of) required input data');
        throw new Error('Incomplete input');
    }
    
    // CXT_THICKNESS
    const RAIL_SECTIONfeatures = cps_RAIL_SECTION.values;
    var value1_c = [...RAIL_SECTIONfeatures]

    const ARP_CUST_SPECfeatures = cps_ARP_CUST_SPEC.values;
    var value2_c = [...ARP_CUST_SPECfeatures]

    const ARP_DRILL_PATTERNfeatures = cps_ARP_DRILL_PATTERN.values;
    var value3_c = [...ARP_DRILL_PATTERNfeatures]

    const ARP_PLUG_TYPEfeatures = cps_ARP_PLUG_TYPE.values;
    var value4_c = [...ARP_PLUG_TYPEfeatures]

    const OA_LENGTH_STRINGfeatures = cps_OA_LENGTH_STRING.values;
    var value5_c = [...OA_LENGTH_STRINGfeatures]

    const ARP_FASTENER_TYPEfeatures = cps_ARP_FASTENER_TYPE.values;
    var value6_c = [...ARP_FASTENER_TYPEfeatures]

    const DESC_UPDATEfeatures = cps_DESC_UPDATE.values;
    var value10_c = [...DESC_UPDATEfeatures]

    // const LBF_PLUG_TEXTfeatures = cps_LBF_PLUG_TEXT.values;
    // var value8_c = [...LBF_PLUG_TEXTfeatures]



    // Concatenate the lagging text
    var value0_c = "PLUG"
    if (value10_c == "Yes"){
        var concat_text = `${value0_c} ${value1_c} ${value2_c} ${value3_c} ${value4_c} ${value5_c} ${value6_c}`;
    }
    else{
        var concat_text = `${value0_c} ${value1_c} ${value2_c} ${value3_c} ${value4_c} ${value5_c} ${value6_c} ${value10_c}`;
    }
    

    const features = cps_LBF_PLUG_TEXT.values;
    var descConds = [...features];
    log.debug('ZLBF_PLUG_TEXT: OUTPUT: cps_LBF_PLUG_TEXT------------>' + descConds);
    descConds.push(concat_text);

    // // Prepare and return
    cps_LBF_PLUG_TEXT.values = descConds;
	
	// log.debug('Calculated descConds' + cps_LBF_PLUG_TEXT.values);
    
    return JSON.stringify({ type: 'vfun', vfunOutput: { result: true, fnArgs: [ cps_LBF_PLUG_TEXT ] } });
}