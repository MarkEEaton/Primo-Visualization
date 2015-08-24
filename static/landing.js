$(document).ready(function(){
	$("#close-overlay").click(function(){
		$("#overlay").hide();
	});
	$("#campus-select").change(function (){
		var campus = $("#campus-select option:selected").text();
		$("#close-overlay").click(function(){
			$("#campus-display").html(campus);
		});
	});
	$("#formsubmit").submit(function(){
		$("#message").empty();
		$("#message").append("<div class='alert alert-success' role='alert'>Loading your data...</div>");
	});
});