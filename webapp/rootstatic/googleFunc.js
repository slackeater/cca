/* ==== Analysis ==== */

function startMetaAnalysis(update, platform){
	if (!update) {
		update = false
	}

	$("#wait1").fadeIn("slow");
	Dajaxice.cloudservice.metadataAnalysis(analysisCallBack,{'tokenID': "aa", 'update': update, 'platform': platform});
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
	$("#searchError").fadeOut("slow");
	Dajaxice.gdrivecloud.fileInfo(showCallBack,{'tokenID': vars['t'], 'id': id})
}

function showCallBack(data){
	Dajax.process(data)
	$("#searchResult").fadeOut("slow")
	$("#fileRevisionContainer").fadeIn("slow")
	$("#searchError").fadeIn("slow");
}

function showRevision(id){
	$("#revisionHistory").fadeIn("slow")
	Dajaxice.gdrivecloud.fileRevision(Dajax.process,{'id': id, 'tokenID': vars['t'], 'importID': vars['i']})
}

/* End */
