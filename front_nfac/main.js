const axios = require('axios').default;

async function fetchNews() {
  try {
    // Replace 'your-api-endpoint' with the actual endpoint URL.
    const response = await axios.get('mytengriapi-production-15d1.up.railway.app');
    
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
