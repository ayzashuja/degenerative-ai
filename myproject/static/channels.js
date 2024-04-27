function redirectToLogin() {
  window.location.href = '/';
}
//
// // JavaScript code to handle logout
// document.getElementById("logoutButton").addEventListener("click", function() {
//   fetch('/logout', {
//       method: 'POST',
//       headers: {
//           'Content-Type': 'application/json'
//       }
//   })
//   .then(response => {
//       // Redirect to login page after logout
//       window.location.href = '/'; 
//   })
//   .catch(error => console.error('Error logging out:', error));
// });
