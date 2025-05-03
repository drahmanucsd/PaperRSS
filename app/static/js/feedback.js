// Handle voting functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add click handlers to all vote links
    document.querySelectorAll('.feedback a').forEach(link => {
        link.addEventListener('click', async function(e) {
            e.preventDefault(); // Prevent default link behavior
            e.stopPropagation(); // Stop event bubbling
            
            // Get the current URL and construct the feedback URL
            const currentUrl = new URL(window.location.href);
            const feedbackUrl = new URL(this.href);
            
            // Ensure we're using HTTPS and the correct port
            feedbackUrl.protocol = 'https:';
            feedbackUrl.hostname = currentUrl.hostname;
            feedbackUrl.port = currentUrl.port;
            
            const feedbackDiv = this.closest('.feedback');
            
            // Disable the link temporarily to prevent double-clicks
            this.style.pointerEvents = 'none';
            
            try {
                const response = await fetch(feedbackUrl.toString(), {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json'
                    },
                    // Allow self-signed certificates in development
                    mode: 'cors',
                    credentials: 'omit'
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                
                // Show success message
                const message = document.createElement('span');
                message.textContent = '✓';
                message.style.color = 'green';
                message.style.marginLeft = '5px';
                feedbackDiv.appendChild(message);
                
                // Remove message after 2 seconds
                setTimeout(() => {
                    message.remove();
                }, 2000);
                
            } catch (error) {
                console.error('Error:', error);
                // Show error message
                const message = document.createElement('span');
                let errorText = 'Error submitting vote. ';
                
                if (error.message.includes('Failed to fetch')) {
                    errorText += 'Please ensure you are accessing the page through https://127.0.0.1:5001 and have accepted the SSL certificate.';
                } else if (error.message.includes('blocked')) {
                    errorText += 'The request was blocked by the browser. Please ensure you are using HTTPS.';
                } else {
                    errorText += 'Please ensure the Flask server is running.';
                }
                
                message.textContent = errorText;
                message.style.color = 'red';
                message.style.marginLeft = '5px';
                message.style.fontSize = '0.8em';
                message.style.display = 'block';
                message.style.marginTop = '5px';
                feedbackDiv.appendChild(message);
                
                // Remove message after 5 seconds
                setTimeout(() => {
                    message.remove();
                }, 5000);
            } finally {
                // Re-enable the link after a short delay
                setTimeout(() => {
                    this.style.pointerEvents = 'auto';
                }, 1000);
            }
        });
    });
}); 