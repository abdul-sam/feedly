BASE_URL = "http://127.0.0.1:8000/";
CSRF_TOKEN = "";
const heartClick = () => {
  CSRF_TOKEN = document.querySelector("[name=csrfmiddlewaretoken]").value;
  let dataset = document.getElementsByClassName("favorite-span")[0].dataset;
  const id = dataset.id;
  const type = dataset.type;
  const favorite = dataset.favorite;
  url = "";
  if (type === "feed") {
    url = `${BASE_URL}api/favorite-feed/${id}/`;
  } else {
    url = `${BASE_URL}api/favorite-category/${id}/`;
  }
  let data = {
    favorite: favorite,
  };
  ajaxRequest(url, "PUT", data).then((data) => {
    let element = document.getElementsByClassName("favorite-span")[0];
    if (data.favorite) {
      updateElement(element, "True", "fa-solid favorite");
    } else {
      updateElement(element, "False", "fa-regular");
    }
    appendFaviroteSection(data);
  });
};

const appendFaviroteSection = (data) => {
  let heading = document.getElementsByClassName("favorite-heading")[0];
  if (data.feeds.length == 0 && data.categories.length == 0) {
    heading.classList.add("d-none");
  } else {
    heading.classList.remove("d-none");
  }

  let favorite_list = document.getElementById("favorite-list");
  let ul =
    '<ul class="nav nav-pills flex-column mb-0 align-items-center align-items-sm-start w-100 pb-2 pt-2 text-dark" id="menu">';

  if (data.feeds.length > 0) {
    data.feeds.map((item) => {
      ul += appendFeed(item);
    });
  }

  if (data.categories.length > 0) {
    data.categories.map((category) => {
      ul += appendCategory(category);
    });
  }
  ul += "</ul>";
  favorite_list.innerHTML = ul;
};

const appendFeed = (item) => {
  image = "";
  if (item.image_url) {
    image = item.image_url;
  } else {
    image = "/static/images/no-image.png";
  }
  feed =  `<li class="nav-item w-100">
            <a href="/feeds/${item.id}" class="nav-link px-0 align-middle main-link text-body fs-12">
              <span class="text-dark p-1">
                <img src="${image}" alt="${item.title}" class="feed-img me-1">
              </span>
              <span class="d-none d-sm-inline">${item.title}</span>
              <span class="text-muted float-end fs-10 p-1">
                ${item.article_count}
              </span>
            </a>
          </li>`;
  return feed;
};

const appendCategory = (category) => {
  category_li = `<li class="nav-item w-100">
                  <span class="">`;

  if (category.feeds.length > 0) {
    category_li += `<span href="#apisubmenu${category.id}" data-bs-toggle="collapse" class="text-dark float-start submenu mt-2">
                      <i class="fa fa-chevron-down"></i>
                    </span>`;
  }

  category_li += `<a href="/categories/${category.id}" class="nav-link px-0 align-middle main-link text-body">
                      <span class="ms-3 d-none d-sm-inline fw-bold">${category.name}</span>
                      <span class="text-muted float-end fs-10 p-1">
                        ${category.total_feed_count}
                      </span>
                    </a>
                  </span>`;

  if (category.feeds.length > 0) {
    category_li += `<ul class="collapse nav flex-column ms-1" id="apisubmenu${category.id}" data-bs-parent="#menu">`;
    category.feeds.map((feed) => {
      category_li += appendFeed(feed);
    });
    category_li += "</ul>";
  }
  category_li += `</li>`;

  return category_li;
};

const appendList = () => {};

const updateElement = (element, favorite, klasses) => {
  element.dataset.favorite = favorite;
  element.innerHTML = `<i class="${klasses} fa-heart"></i>`;
};

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
