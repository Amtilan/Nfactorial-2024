const axios = require('axios').default;

async function fetchNews() {
  try {
    // Replace 'your-api-endpoint' with the actual endpoint URL.
    const response = await axios.get('http://127.0.0.1:8000/news');
    
    // Assuming the response is in the format of the provided JSON data:
    // {
    //   "id": 1,
    //   "data": [ ... ] 
    // }
    const articles = response.data.data;
    
    // Log the title of each article.
    articles.forEach(article => {
      console.log(`Title: ${article.title}`);
    });
  } catch (error) {
    console.error('Error fetching news:', error);
  }
}

// Call the function to fetch news.
fetchNews();
