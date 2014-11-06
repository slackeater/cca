/* ==== Analysis ==== */

function startMetaAnalysis(update){
	if (!update) {
		update = false
	}

	$("#wait1").fadeIn("slow");
	Dajaxice.gdrivecloud.analyzeMetaData(analysisCallBack,{'importID': vars['i'],'tokenID': vars['t'], 'update': update});
}

// callback for analysis
function analysisCallBack(data){
 	Dajax.process(data)
	$("#wait1").fadeOut("slow");
	$("#metaAnalysis").fadeIn("slow");
}
