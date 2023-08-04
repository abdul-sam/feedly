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
      updateElement(element, "True", "fa-solid color-green");
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
  image = item.image_url ? item.image_url : "/static/images/no-image.png"
  feed = `<li class="nav-item w-100">
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

const readLaterClick = (event) => {
  CSRF_TOKEN = document.querySelector("[name=csrfmiddlewaretoken]").value;
  let element = event.target.parentElement.closest(".read-later-span");
  let dataset = element.dataset;
  const id = dataset.id;
  const read_later = dataset.readlater;
  url = `${BASE_URL}api/article/${id}/read-later/`;
  let data = {
    readLater: read_later,
  };
  ajaxRequest(url, "PUT", data).then((data) => {
    elements = document.querySelectorAll(".read-later-span")
    Array.from(elements).map((item) => {
      if(item.dataset.id == element.dataset.id){
        if (data.read_later) {
          updateReadLaterElement(item, "True", "fa-solid color-green");
        } else {
          updateReadLaterElement(item, "False", "fa-regular");
        }
      }
    })
  });
};

const updateReadLaterElement = (element, read_later, klasses) => {
  element.dataset.readlater = read_later;
  element.innerHTML = `<i class="${klasses} fa-bookmark"></i>`;
};

const recentlyReadClick = (event) => {
  CSRF_TOKEN = document.querySelector("[name=csrfmiddlewaretoken]").value;
  let element = event.target.parentElement.closest(".recently-read-span");
  let dataset = element.dataset;
  const id = dataset.id;
  const recently_read = dataset.recentlyread;
  url = `${BASE_URL}api/article/${id}/recently-read/`;
  let data = {
    recentlyRead: recently_read,
  };
  ajaxRequest(url, "PUT", data).then((data) => {
    elements = document.querySelectorAll(".recently-read-span")
    Array.from(elements).map((item) => {
      if(item.dataset.id == element.dataset.id){
        if (data.recently_read) {
          updateRecentlyReadElement(item, "True", "fa-check-double color-green");
        } else {
          updateRecentlyReadElement(item, "False", "fa-check");
        }
      }
    })
  });
};

const updateRecentlyReadElement = (element, recently_read, klasses) => {
  element.dataset.recentlyread = recently_read;
  element.innerHTML = `<i class="fa solid ${klasses}"></i>`;
};

const articleClick = (event) => {
  debugger;
  let dataset = event.target.parentElement.dataset;
  const id = dataset.id;
  url = `${BASE_URL}api/article/${id}/`;
  setTimeout(() => {
    appendArticle(url)
  }, 1000)
};

const appendArticle = (url) => {
  getAjaxRequest(url, "GET").then((data) => {
    let content = "";
    let actions = "";
    let articleActions = document.getElementById("articleActions");
    let articleContent = document.getElementById("articleContent");

    actions += `<span 
                  class="p-1 px-2 cursor-pointer read-later-span" 
                  data-readLater="${data.read_later ? 'True' : 'False'}" 
                  data-id="${data.id}" onclick="readLaterClick(event);"
                >`;

    if (data.read_later) {
      actions += '<i class="fa-solid fa-bookmark color-green"></i>';
    } else {
      actions += `<i class="fa-regular fa-bookmark text-dark"></i>`;
    }
    actions += "</span>";

    actions += `<span 
                  class="p-1 px-2 cursor-pointer recently-read-span" 
                  data-recentlyread="${data.recently_read ? 'True' : 'False'}" 
                  data-id="${data.id}" onclick="recentlyReadClick(event);"
                >`;

    if (data.recently_read) {
      actions += `<i class="fa-solid fa-check-double color-green"></i>`;
    } else {
      actions += `<i class="fa-solid fa-check text-dark"></i>`;
    }
    actions += "</span>";

    actions +=
      '<span class="p-1 px-2 cursor-pointer"><i class="fa-regular fa-star"></i></span>';

    date = new Date(data.created_at.replace('T', ' '));
    articleDate = `${date.toDateString()} at ${date.toLocaleTimeString()}`
    let description = descriptionParser(feed.description)
    content += `<h4 class="modal-title">${data.title}</h4>`;
    content += `<small class="mt-2 mb-5 text-muted fs-12">
                  <a href="" class="text-decoration-none">
                    <span>${data.feed.article_count}</span> ${data.feed.title} | 
                  </a>
                  <span>${articleDate}</span>
                </small>`;
    content += `<img src="${data.image_url}" class="mt-4"/>`;
    content += `<div id="articleDescription" class="mt-4">
                  ${description}
                </div>`;

    content += `<span class="mb-5">
                  <a href="${data.link}" class="text-decoration-none text-muted fw-bold fs-12 pb-5" target="_blank">
                    <div class="card mt-5">
                      <div class="card-body text-center">
                        VISIT WEBSITE
                      </div>
                    </div>
                  </a>
                </span>`;

    articleActions.innerHTML = actions;
    articleContent.innerHTML = content;
    console.log("Data: ", data);
  });
}

