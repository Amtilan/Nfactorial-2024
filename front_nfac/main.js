
function insertHtml(content) {
  document.getElementsByClassName("three-column_main main-news_super").innerHTML += content;
}

function createNewsItem(news) {
  return `
      <div class="news-item">
          <a href="${news.url}">
              <picture>
                  <img src="${news.image}">
              </picture>
              <h2>${news.title}</h2>
          </a>
          <time>${news.date_time}</time>
      </div>
  `;
}

function fetchAndDisplayNews() {
  axios.get('https://mytengriapi-production-15d1.up.railway.app/')
      .then(function (response) {
          const newsItems = response.data['0']['data'];
          newsItems.forEach(news => {
            console.log(news);
              const newsHtml = createNewsItem(news);
              insertHtml(newsHtml);
          });
      })
      .catch(function (error) {
          console.error('Ошибка при получении данных:', error);
      });
}

document.addEventListener('DOMContentLoaded', fetchAndDisplayNews);

// Call the function to fetch news.
fetchNews();
