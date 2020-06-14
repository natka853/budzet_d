function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function downloadBlob(blob, filename) {
    const a = document.createElement("a");
    a.style = "display: none";
    const url = window.URL.createObjectURL(blob);
    a.setAttribute("href", url);
    a.setAttribute("download", filename);
    document.getElementsByTagName("body")[0].append(a);
    a.click();
    window.URL.revokeObjectURL(url);
    a.remove();
}

function viewBlob(blob) {
    const url = window.URL.createObjectURL(blob);
    const newTab = window.open(url, '_blank');
    newTab.focus();
}

function generatePdf(requestUrl, searchResult, title, isDownload) {
    let download = isDownload;
    if (download === undefined) {
        download = false;
    }

    const csrfToken = getCookie('csrftoken');
    const request = new Request(
        requestUrl,
        {
            headers: {
                'X-CSRFToken': csrfToken,
                "Content-Type": "application/json; charset=utf-8"
            }
        }
    );

    const currentUrl = new URL(window.location.href);
    const currentUrlSearchParameters = currentUrl.searchParams;

    const searchParameters = {
        nameContains: currentUrlSearchParameters.get("name_contains"),
        idExact: currentUrlSearchParameters.get("id_exact"),
        descriptionContains: currentUrlSearchParameters.get("description_contains"),
        kwotaMin: currentUrlSearchParameters.get("kwota_min"),
        kwotaMax: currentUrlSearchParameters.get("kwota_max"),
        dateMin: currentUrlSearchParameters.get("date_min"),
        dateMax: currentUrlSearchParameters.get("date_max"),
        inputState: currentUrlSearchParameters.get("zrodlo")
    };

    const requestBody = {searchResult: searchResult, searchParameters: searchParameters, title: title};

    fetch(request, {
        method: 'POST',
        mode: 'same-origin',  // Do not send CSRF token to another domain.
        body: JSON.stringify(requestBody)
    }).then(function (response) {
        const filename = response.headers.get('Content-Disposition').split("filename=")[1].split("\"").join("");
        response.blob().then(blob => {
            if (download) {
                downloadBlob(blob, filename);
            } else {
                viewBlob(blob);
            }
        });
    });
}