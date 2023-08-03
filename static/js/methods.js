let ajaxRequest = async (url = "", method = "", data = {}) => {
  const response = await fetch(url, {
    method: method,
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": CSRF_TOKEN,
    },
    body: JSON.stringify(data),
  });
  return response.json();
};

let getAjaxRequest = async (url = "") => {
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  return response.json();
};

const descriptionParser = (description) => {
  return description.replace(/<img[^>]*>/g, "");
}

const preventClose = (event) => {
  event.target.parentElement.querySelector('.follow-list-dd').addEventListener('click', function(event) {
    event.stopPropagation();
  });
}