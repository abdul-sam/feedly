const followClick = (event) => {
  let element = event.target.parentElement.closest(".url");
  let dataset = element.dataset;

  let url = `${BASE_URL}${dataset.url}/`;

  // Temporary block
  let data = {
    user_id: dataset.user,
  };
  // Temporary block end

  ajaxRequest(url, "PUT", data).then((data) => {
    let ul = `<li class="nav-item w-100">
        <a href="folders" class="nav-link px-0 align-middle main-link text-body">
          <i class="fa-solid fa-bars fs-16"></i>
          <span class="ms-3 d-none d-sm-inline fw-bold fw-bold">All</span>
          <span class="text-muted float-end fs-10 p-1">
            ${data.total_feeds}
          </span>
        </a>
      </li>`;

    if (data.folders.length > 0) {
      data.folders.map((folder) => {
        ul += appendFolder(folder);
      });
    }

    ul += `<li class="w-100">
            <a href="#" class="nav-link align-middle text-body px-4 mt-3 py-1">
              <span class="ms-1 d-none d-sm-inline" data-bs-toggle="modal" data-bs-target="#folderModal">Create Folder</span>
            </a>
          </li>`

    let feed_list = document.getElementById("feed--list");
    feed_list.innerHTML = ul;
  });
};

const appendFolder = (folder) => {
  let folder_li = `<li class="nav-item w-100">
                    <span class="">
                      <span href="#apisubmenu${folder.id}" data-bs-toggle="collapse" class="text-dark float-start submenu mt-2">
                        <i class="fa fa-chevron-down"></i>
                      </span>
                      <a href="/folders/${folder.id}" class="nav-link px-0 align-middle main-link text-body">
                        <span class="ms-3 d-none d-sm-inline fw-bold">${folder.name}</span>
                        <span class="text-muted float-end fs-10 p-1">
                          ${folder.total_article_count}
                        </span>
                      </a>
                    </span>`;

  if (folder.feeds.length > 0) {
    folder_li += `<ul class="collapse nav flex-column ms-1" id="apisubmenu${folder.id}" data-bs-parent="#menu">`;
    folder.feeds.map((feed) => {
      folder_li += appendFeed(feed);
    });
    folder_li += "</ul>";
  }
  folder_li += `</li>`;

  return folder_li;
};
