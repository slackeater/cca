/* ==== Analysis ==== */

function startMetaAnalysis(){
	$("#wait1").fadeIn("slow");
	Dajaxice.gdrivecloud.analyzeMetaData(analysisCallBack,{'importID': vars['i'],'tokenID': vars['t']});
}

// callback for analysis
function analysisCallBack(data){
 	Dajax.process(data)
	$("#wait1").fadeOut("slow");
	$("#metaAnalysis").fadeIn("slow");
}
