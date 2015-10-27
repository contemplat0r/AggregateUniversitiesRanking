
/////////////////////////////////////////////
//Check OnKeyPress
/////////////////////////////////////////////

	function checkempty(id){
		var aa = document.getElementById(id);
		var bb = document.getElementById(id + "Error");
		aa.style.background="#FFFFFF";
		bb.style.display="none";
	}
	
/////////////////////////////////////////////
//Registration
/////////////////////////////////////////////

	function registration2_checkout(){
		var withError = false;
		
		if(registration2_checkfirstname()){ 
			withError = true;
		}
		
		if(registration2_checkfamilyname()) {
			withError = true;
		}
		if(registration2_checkptitle()) {
			withError = true;
		}

		if(registration2_checkjobposition()) {
			withError = true;
		}

		if(registration2_checkdepartment()) {
			withError = true;
		}

		if(registration2_checkcity()) {
			withError = true;
		}

		if(registration2_checkcountry()) {
			withError = true;
		}

		if (registration2_checkemail()){
			withError = true;
		}

		
		if(registration2_checkphoneno3()) {
			withError = true;
		}
		
		var code = "";
		for (var i=0;i<document.registrationForm.accomodation.length;i++) {
			if (document.registrationForm.accomodation[i].checked) {
				code = document.registrationForm.accomodation[i].value;
			}
		}
		if (code=="yes") {
			
		} else if (code=="no") {
		
				if (registration2_checkeventfrom()){
					withError = true;
				}
				
				if(registration2_checkroomnumber()){
					withError = true;
				}
			
		}
		
		if (!withError) {
			document.getElementById('registrationForm').submit();
		}
	}
	
	function registration2_viewinfo(){
		var withError = false;
		if(registration2_checkviewinfo()) {
			withError = true;
		}
		if (!withError) {
			document.getElementById('viewinfoForm').submit();
		}
		
	}
	
	function registration2_checkpromotion() {
		var code = "";
		for (var i=0;i<document.registrationForm.accomodation.length;i++) {
			if (document.registrationForm.accomodation[i].checked) {
				//alert("fgr");
				code = document.registrationForm.accomodation[i].value;
			}
		}
		if (code=="yes") {
			
			document.getElementById("eventfrom").disabled=true;
			document.getElementById("q1").disabled=true;
			document.getElementById("q2").disabled=true;
			document.getElementById("roomnumber").disabled=true;
			var eventfrom= document.getElementById("eventfrom");
			var eventfromError= document.getElementById("eventfromError");
			eventfrom.style.background="#FFFFFF";
			eventfromError.style.display="none";
			withError = false;
			return withError;
			
			
		} else if (code=="no") {
			//alert(code);
			document.getElementById("eventfrom").disabled=false;
			document.getElementById("q1").disabled=false;
			document.getElementById("q2").disabled=false;
			//document.getElementById("total").disabled=false;
			document.getElementById("roomnumber").disabled=false;
			//var eventfrom= document.getElementById("eventfrom");
			//if(eventfrom.selectedIndex == 0) {
			//	document.getElementById("q1").disabled=true;
			//	document.getElementById("q2").disabled=true;
			//	document.getElementById("roomnumber").disabled=true;
			//}else{
			//	document.getElementById("q1").disabled=false;
			//	document.getElementById("q2").disabled=false;
			//	document.getElementById("roomnumber").disabled=false;
				//}
		}
		
		else{}
	}
	
	function checkeventfrom() {
		if(document.getElementById("100T500").value=="500"){
			document.getElementById("tb1").style.display="block";
			document.getElementById("tb2").style.display="block";
			document.getElementById("tb3").style.display="block";

		}
		else {
			document.getElementById("tb1").style.display="block";
			document.getElementById("tb2").style.display="none";
			document.getElementById("tb3").style.display="block";
			 
			
		}
	}
	
	function checkcriteria(){
		 var stl=stl = 'block';

		    var tbl  = document.getElementById('UniversityRanking');
		    var rows = tbl.getElementsByTagName('tr');
		    

		if(document.getElementById("criteria").value=="alumni"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[5].style.display=stl;
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		        cels[9].style.display="none";
		        cels[10].style.display="none";
		    }
			
		}
		else if(document.getElementById("criteria").value=="award"){

		    for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[5].style.display="none";
		        cels[6].style.display=stl;
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		        cels[9].style.display="none";
		        cels[10].style.display="none";
		        
		    }
			
		}
		else if(document.getElementById("criteria").value=="hici"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display=stl
		        cels[8].style.display="none";
		        cels[9].style.display="none";
		        cels[10].style.display="none";
		    }
	
		}
		else if(document.getElementById("criteria").value=="ns"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display=stl;
		        cels[9].style.display="none";
		        cels[10].style.display="none";
		    }
	
		}
		else if(document.getElementById("criteria").value=="pub"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		        cels[9].style.display=stl;
		        cels[10].style.display="none";
		    }
	
		}
		else if(document.getElementById("criteria").value=="pcp"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		        cels[9].style.display="none";
		        cels[10].style.display=stl;
		    }
	
		}
		
	}
	
	function checkcriteria2(){
		 var stl=stl = 'block';

		    var tbl  = document.getElementById('UniversityRanking');
		    var rows = tbl.getElementsByTagName('tr');
		    

		if(document.getElementById("criteria").value=="alumni"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display=stl;
		        cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		        cels[9].style.display="none";
		    }
			
		}
		else if(document.getElementById("criteria").value=="award"){

		    for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display="none";
		        cels[5].style.display=stl;
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		        cels[9].style.display="none";
		        
		    }
			
		}
		else if(document.getElementById("criteria").value=="hici"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display="none";
		        cels[5].style.display="none";
		        cels[6].style.display=stl
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		        cels[9].style.display="none";
		    }
	
		}
		else if(document.getElementById("criteria").value=="ns"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display="none";
		        cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display=stl;
		        cels[8].style.display="none";
		        cels[9].style.display="none";
		    }
	
		}
		else if(document.getElementById("criteria").value=="pub"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display="none";
		        cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display=stl;
		        cels[9].style.display="none";
		    }
	
		}
		else if(document.getElementById("criteria").value=="pcp"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display="none";
		        cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		        cels[9].style.display=stl;
		    }
	
		}
		
	}
	
	
	function checkcriteria3(){
		 var stl=stl = 'block';

		    var tbl  = document.getElementById('UniversityRanking');
		    var rows = tbl.getElementsByTagName('tr');
		    

		if(document.getElementById("criteria").value=="alumni"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display=stl;
		        cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		    }
			
		}
		else if(document.getElementById("criteria").value=="hici"){

		    for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display="none";
		        cels[5].style.display=stl;
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		        
		    }
			
		}
		else if(document.getElementById("criteria").value=="ns"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display="none";
		        cels[5].style.display="none";
		        cels[6].style.display=stl
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		    }
	
		}
		else if(document.getElementById("criteria").value=="pub"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display="none";
		        cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display=stl;
		        cels[8].style.display="none";
		    }
	
		}
		else if(document.getElementById("criteria").value=="pcp"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display="none";
		        cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display=stl;
		    }
	
		}
		
	}
	
	function checkcriteria4(){
		 var stl=stl = 'block';

		    var tbl  = document.getElementById('UniversityRanking');
		    var rows = tbl.getElementsByTagName('tr');
		    

		if(document.getElementById("criteria").value=="alumni"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display=stl;
		        cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		    }
			
		}
		else if(document.getElementById("criteria").value=="award"){

		    for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display="none";
		        cels[5].style.display=stl;
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		        
		    }
			
		}
		else if(document.getElementById("criteria").value=="hici"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display="none";
		        cels[5].style.display="none";
		        cels[6].style.display=stl
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		    }
	
		}
		else if(document.getElementById("criteria").value=="pub"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display="none";
		        cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display=stl;
		        cels[8].style.display="none";
		    }
	
		}
		else if(document.getElementById("criteria").value=="top"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display="none";
		        cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display=stl;
		    }
	
		}
		
	}





















function checkcriteriaExcludingAward(){
		 var stl=stl = 'block';

		    var tbl  = document.getElementById('UniversityRanking');
		    var rows = tbl.getElementsByTagName('tr');
		    

		if(document.getElementById("criteria").value=="alumni"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[5].style.display=stl;
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		        cels[9].style.display="none";
		        cels[10].style.display="none";
				cels[11].style.display="none";
		    }
			
		}
		else if(document.getElementById("criteria").value=="award"){

		    for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[5].style.display="none";
		        cels[6].style.display=stl;
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		        cels[9].style.display="none";
		        cels[10].style.display="none";
				cels[11].style.display="none";
		        
		    }
			
		}
		else if(document.getElementById("criteria").value=="hici"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display=stl
		        cels[8].style.display="none";
		        cels[9].style.display="none";
		        cels[10].style.display="none";
				cels[11].style.display="none";
		    }
	
		}
		else if(document.getElementById("criteria").value=="ns"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display=stl;
		        cels[9].style.display="none";
		        cels[10].style.display="none";
				cels[11].style.display="none";
		    }
	
		}
		else if(document.getElementById("criteria").value=="pub"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		        cels[9].style.display=stl;
		        cels[10].style.display="none";
				cels[11].style.display="none";
		    }
	
		}
		else if(document.getElementById("criteria").value=="pcpa"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		        cels[9].style.display="none";
		        cels[10].style.display=stl;
				cels[11].style.display="none";
		    }
	
		}
		else if(document.getElementById("criteria").value=="pcpb"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        cels[8].style.display="none";
		        cels[9].style.display="none";
		        cels[10].style.display="none";
				cels[11].style.display=stl;
		    }
	
		}
		
	}






































	
	function checkcriteria5(){
		 var stl=stl = 'block';

		    var tbl  = document.getElementById('UniversityRanking');
		    var rows = tbl.getElementsByTagName('tr');
		    

		if(document.getElementById("criteria").value=="hici"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display=stl;
		        cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		    }
			
		}
		else if(document.getElementById("criteria").value=="pub"){

		    for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display="none";
		        cels[5].style.display=stl;
		        cels[6].style.display="none";
		        cels[7].style.display="none";
		        
		    }
			
		}
		else if(document.getElementById("criteria").value=="top"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display="none";
		        cels[5].style.display="none";
		        cels[6].style.display=stl
		        cels[7].style.display="none";
		    }
	
		}
		else if(document.getElementById("criteria").value=="fund"){
			for (var row=1; row<(rows.length);row++) {
		    	var cels = rows[row].getElementsByTagName('td');
		    	cels[4].style.display="none";
		        cels[5].style.display="none";
		        cels[6].style.display="none";
		        cels[7].style.display=stl;
		    }
	
		}
		
	}
	
	
	
function registration2_checkeventfrom() {
		
		var withError = false;
		var eventfrom= document.getElementById("eventfrom");
		var eventfromError= document.getElementById("eventfromError");
		
		if(eventfrom.selectedIndex == 0) {
			
			eventfrom.style.background="#FED2FE";
			eventfromError.innerHTML="<span class='form_error_message'>Select one option</span>";
			eventfromError.style.display="block";
			withError= true;
		} else{
			
			eventfrom.style.background="#FFFFFF";
			eventfromError.style.display="none";
			withError = false;
		}
		return withError;
	}
	
	function checkAccompanyempty(id){
		var aa = document.getElementById(id);
		if(aa=="")
		{
			document.getElementById("ds21").disabled=true;
		}
	}
	
	
	
	function registration2_checkAccompanying(){

		var addfirstnamevalue = document.getElementById("addfirstname");
			
		if(addfirstnamevalue!="")
		{
			document.getElementById("ds21").disabled=false;
			
		}
	
	}
	
	function registration2_checkaddsalutation(){
		if (document.getElementById("addsalutation").value=="Please Choose..."){
			document.getElementById("addfirstname").disabled=true;
			document.getElementById("addfamilyname").disabled=true;
		}else{
			document.getElementById("addfirstname").disabled=false;
			document.getElementById("addfamilyname").disabled=false;
		}
	}
	
	
		
	function registration2_checkptitle(){
		var withError = false;
		var ptitle= document.getElementById("ptitle");
		var ptitleError= document.getElementById("ptitleError");
		
		if(ptitle.selectedIndex == 0) {
			ptitle.style.background="#FED2FE";
			ptitleError.innerHTML="<span class='form_error_message'>Select one option</span>";
			ptitleError.style.display="block";
			withError= true;
		} else{
			ptitle.style.background="#FFFFFF";
			ptitleError.style.display="none";
			withError = false;
		}
		return withError;
	}

	function registration2_checkfirstname(){
		
		var withError=false;
		var firstnameError = document.getElementById("firstnameError");
		var firstname = document.getElementById("firstname");
		if(firstname.value==""){
			firstname.style.background="#FED2FE";
			firstnameError.innerHTML="<span class='form_error_message'>First name is required</span>";
			firstnameError.style.display="block";
			withError= true;
		}else{
			firstname.style.background="#FFFFFF";
			firstnameError.style.display="none";
			withError= false;
		}
		return withError;
	}

	function registration2_checkfamilyname(){
		
		var withError=false;
		var familynameError = document.getElementById("familynameError");
		var familyname = document.getElementById("familyname");
		if(familyname.value==""){
			familyname.style.background="#FED2FE";
			familynameError.innerHTML="<span class='form_error_message'>Family name is required</span>";
			familynameError.style.display="block";
			withError= true;
		}else{
			familyname.style.background="#FFFFFF";
			familynameError.style.display="none";
			withError= false;
		}
		return withError;
	}

	function registration2_checkjobposition(){
		
		var withError=false;
		var jobpositionError = document.getElementById("jobpositionError");
		var jobposition = document.getElementById("jobposition");
		if(jobposition.value==""){
			jobposition.style.background="#FED2FE";
			jobpositionError.innerHTML="<span class='form_error_message'>Position is required</span>";
			jobpositionError.style.display="block";
			withError= true;
		}else{
			jobposition.style.background="#FFFFFF";
			jobpositionError.style.display="none";
			withError= false;
		}
		return withError;
	}

	function registration2_checkdepartment(){
		
		var withError=false;
		var departmentError = document.getElementById("departmentError");
		var department = document.getElementById("department");
		if(department.value==""){
			department.style.background="#FED2FE";
			departmentError.innerHTML="<span class='form_error_message'>Institution is required</span>";
			departmentError.style.display="block";
			withError= true;
		}else{
			department.style.background="#FFFFFF";
			departmentError.style.display="none";
			withError= false;
		}
		return withError;
	}

	function registration2_checkaddress(){
		
		var withError=false;
		var addressError = document.getElementById("addressError");
		var address = document.getElementById("address");
		if(address.value==""){
			address.style.background="#FED2FE";
			addressError.innerHTML="<span class='form_error_message'>Street Address is required</span>";
			addressError.style.display="block";
			withError= true;
		}else{
			address.style.background="#FFFFFF";
			addressError.style.display="none";
			withError= false;
		}
		return withError;
	}
		
	function registration2_checkcountry(){
		var withError = false;
		var country= document.getElementById("country");
		var countryError= document.getElementById("countryError");
		
		if(country.selectedIndex == 0) {
			country.style.background="#FED2FE";
			countryError.innerHTML="<span class='form_error_message'>Select one option</span>";
			countryError.style.display="block";
			withError= true;
		} else{
			country.style.background="#FFFFFF";
			countryError.style.display="none";
			withError = false;
		}
		return withError;
	}

	function registration2_checkcity(){
		
		var withError=false;
		var cityError = document.getElementById("cityError");
		var city = document.getElementById("city");
		if(city.value==""){
			city.style.background="#FED2FE";
			cityError.innerHTML="<span class='form_error_message'>City is required</span>";
			cityError.style.display="block";
			withError= true;
		}else{
			city.style.background="#FFFFFF";
			cityError.style.display="none";
			withError= false;
		}
		return withError;
	}

	function registration2_checkstate(){
		

		var withError=false;
		var stateError = document.getElementById("stateError");
		var state = document.getElementById("state");
		if(state.value==""){
			state.style.background="#FED2FE";
			stateError.innerHTML="<span class='form_error_message'>State is required</span>";
			stateError.style.display="block";
			withError= true;
		}else{
			state.style.background="#FFFFFF";
			stateError.style.display="none";
			withError= false;
		}
		return withError;
	}
	
	function registration2_checkroomnumber(){
		var withError = false;
		var w = /^[0-9]*$/;
		var roomnumberError = document.getElementById("roomnumberError");
		var roomnumber = document.getElementById("roomnumber");
		
		if(roomnumber.value==""){
			roomnumber.style.background="#FED2FE";
			roomnumberError.innerHTML="<span class='form_error_message'>Number of Rooms is required</span>";
			roomnumberError.style.display="block";
			withError= true;
		}else if(roomnumber.value.match(w)==null){
			roomnumber.style.background="#FED2FE";
			roomnumberError.innerHTML="<span class='form_error_message'>Room number is invalid. Please input numeric only</span>";
			roomnumberError.style.display="block";
			withError =true;
		}
		else{
			roomnumber.style.background="#FFFFFF";
			roomnumberError.style.display="none";
			withError= false;
		}
		return withError;
	}
	
	
	function registration2_checkphoneno3(){
		var withError = false;
		var u = /^[0-9]*$/;
		var phonenoError = document.getElementById("phoneno3Error");
		var phoneno3 = document.getElementById("phoneno3");
		if (phoneno3.value =="" ) {
			phoneno3.style.background="#FED2FE";
			phonenoError.innerHTML="<span class='form_error_message'>Phone number is required</span>";
			phonenoError.style.display="block";
			withError =true;
		} else if(phoneno3.value.match(u)==null){
			phoneno3.style.background="#FED2FE";
			phonenoError.innerHTML="<span class='form_error_message'>Phone number is invalid. Please input numeric only</span>";
			phonenoError.style.display="block";
			withError =true;
		}else{
			phoneno3.style.background="#FFFFFF";
			phonenoError.style.display="none";
			withError =false;
		}
		return withError;
	}
	
	function registration2_checkemail(){
		var withError=false;
		var u = /^[-a-zA-Z0-9_\.]+@[-a-zA-Z0-9_\.]+[\.a-zA-Z]+$/;
		var emailaddressError = document.getElementById("emailaddressError");
		var emailaddress = document.getElementById("emailaddress");
		if(emailaddress.value==""){
			emailaddress.style.background="#FED2FE";
			emailaddressError.innerHTML="<span class='form_error_message'>Email address is required</span>";
			emailaddressError.style.display="block";
			withError= true;
		}else if(emailaddress.value.match(u)==null){
			emailaddress.style.background="#FED2FE";
			emailaddressError.innerHTML="<span class='form_error_message'>Email address is invalid</span>";
			emailaddressError.style.display="block";
			withError= true;
		}else{
			emailaddress.style.background="#FFFFFF";
			emailaddressError.style.display="none";
		}
		return withError;
	}
	
	function registration2_checkviewinfo(){
		var withError=false;
		var u = /^[-a-zA-Z0-9_\.]+@[-a-zA-Z0-9_\.]+[\.a-zA-Z]+$/;
		var viewinfoError = document.getElementById("viewinfoError");
		var viewinfo = document.getElementById("viewinfo");
		if(viewinfo.value==""){
			viewinfo.style.background="#FED2FE";
			viewinfoError.innerHTML="<span class='form_error_message'>Email address is required</span>";
			viewinfoError.style.display="block";
			withError= true;
		}else if(viewinfo.value.match(u)==null){
			viewinfo.style.background="#FED2FE";
			viewinfoError.innerHTML="<span class='form_error_message'>Email address is invalid</span>";
			viewinfoError.style.display="block";
			withError= true;
		}else{
			viewinfo.style.background="#FFFFFF";
			viewinfoError.style.display="none";
		}
		return withError;
		
	}

	function registration2_reset(){
		document.getElementById('registration2Form').reset();
		registration2_checkpromotion();
	}
	


