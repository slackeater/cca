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

/* === Search === */

function startRes(){
	$("#wait2").fadeIn("slow");
	$("#searchError").fadeOut("slow");
	Dajaxice.gdrivecloud.searchMetaData(resCallBack, {'tokenID': vars['t'], 'form': $("#searchForm").serialize(true)})
}

function resCallBack(data){
	Dajax.process(data)
	$("#wait2").fadeOut("slow");
	$("#searchRes").fadeIn("slow");
	$("#searchError").fadeIn("slow");
}

function showFile(id){
	//loader
	$("#"+id).attr("src","/static/477.GIF").fadeIn("slow")
	//$("#"+id+"-load").fadeIn("fast")
	//Dajaxice.gdrivecloud.fileInfo(showCallBack,{'tokenID': vars['t'], 'id': id})
}

function showCallBack(data){
	Dajax.process(data)

}
/* End */
