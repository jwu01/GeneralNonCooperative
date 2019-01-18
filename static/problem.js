var editorElement = document.getElementById("editor")
var json = JSON.parse(document.getElementById("problem").textContent);
var errorArea = document.getElementById("error")
document.getElementById('title').textContent = json.name
// document.getElementById('title').textContent = json.name.charAt(0).toUpperCase() + json.name.slice(1)
var getFunctionBase = () => {
            	return `function ${json.name} (input) {
	return
}`
            }
editorElement.textContent = getFunctionBase();
var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.getSession().setMode("ace/mode/javascript");
document.getElementById('editor').style.fontSize='16px';

description = json.description;
document.getElementById('problemDescription').textContent = description
var tableVisible = document.getElementById('testCases');
var tableHidden = document.getElementById('hiddenTestCases');
var getTableRow = (input, output) => {
	return `<tr>
<td>${input}</td>
<td>${output}</td>
<td id='output${input}'></td>
<td><i id='result${input}'></i></td>
</tr>`
}

var getTableRowHidden = (input, output) => {
    return `<tr>
<td>${output}</td>
<td id='outputHidden${input}'></td>
<td><i id='resultHidden${input}'></i></td>
</tr>`
}

Object.keys(json.testCases).forEach((i) => {
    tableVisible.innerHTML += getTableRow(i, json.testCases[i])
})

Object.keys(json.hiddenTestCases).forEach((i) => {
    tableHidden.innerHTML += getTableRowHidden(i, json.hiddenTestCases[i])
})

document.getElementById('submit').addEventListener('click', () => {
    var showConfetti = true;
    errorArea.textContent = "";
	Object.keys(json.testCases).forEach((i) => {
    	var expected = json.testCases[i];
        try {
        	var returned = eval(editor.getValue() + `${json.name}(${i})`)
        } catch (e) {
        	errorArea.textContent = e; 2
        }
    	if (returned != expected) {
    		showConfetti = false;			
    	}
        returned = returned.toString()
        var resultsElement = document.getElementById(`result${i}`)
        if (returned.indexOf(',') > -1) {
            returned = `[${returned.trim()}]`
        } 
    	document.getElementById(`output${i}`).textContent = returned == null ? 'Null' : returned
        var resultText = (returned == expected) ? 'Pass' : 'Fail'
        resultsElement.textContent = resultText
        if (resultText == 'Pass') {
            if (resultsElement.classList.contains('fail'))
                resultsElement.classList.remove('fail')
            if (!resultsElement.classList.contains('pass'))
                resultsElement.classList.add('pass')
        } else {
            if (resultsElement.classList.contains('pass'))
                resultsElement.classList.remove('pass')
            if (!resultsElement.classList.contains('fail'))
                resultsElement.classList.add('fail')
        }
    })

    Object.keys(json.hiddenTestCases).forEach((i) => {
        var expected = json.hiddenTestCases[i];
        
        try {
            var returned = eval(editor.getValue() + `${json.name}(${i})`)
        } catch (e) {
            errorArea.textContent = e;
        }
        if (returned != expected) {
            showConfetti = false;
        }

        returned = returned.toString()
        var resultsElement = document.getElementById(`resultHidden${i}`)
        console.log(`[${returned}]`)
        console.log(expected)
        if (returned.indexOf(',') > -1) {
            returned = `[${returned.trim()}]`
        } 
        var resultText = (returned == expected) ? 'Pass' : 'Fail'
        document.getElementById(`outputHidden${i}`).textContent = returned == null ? 'Null' : returned
        resultsElement.textContent = resultText
        if (resultText == 'Pass') {
            if (resultsElement.classList.contains('fail'))
                resultsElement.classList.remove('fail')
            if (!resultsElement.classList.contains('pass'))
                resultsElement.classList.add('pass')
        } else {
            if (resultsElement.classList.contains('pass'))
                resultsElement.classList.remove('pass')
            if (!resultsElement.classList.contains('fail'))
                resultsElement.classList.add('fail')
        }
    })



    if (showConfetti) {
    	StartConfetti();
    	setTimeout(function () {window.location.href = `/success?title=${json.name}`;}, 5000)

    }
})
