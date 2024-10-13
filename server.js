const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
const PORT = 8080;

// Use middleware
app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.urlencoded({ extended: true }));

// Store users in memory (for simplicity; in a real app, use a database)
let users = [];

// Serve login page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});


// Serve singup page with the custom of the post meth
app.get('/signup', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'signup.html'));
});

// Handle signup form submission
app.post('/signup', (req, res) => { 
    const { name, email, password, phone } = req.body;

    // Check if user already exists
    const userExists = users.find(user => user.email === email);
    if (userExists) {
        return res.redirect('/signup?error=User already exists');
    }

    // Save new user
    users.push({ name, email, password, phone });
    console.log(`New user registered: ${name} (${email})`);

    // Redirect to login page after signup
    res.redirect('/?message=Signup successful, please log in');
});

// Handle login form submission
app.post('/login', (req, res) => {
    const { email, password } = req.body;

    // Check if user exists and password matches in the existance of the form
    const user = users.find(user => user.email === email && user.password === password);

    if (user) {
        // Redirect to dashboard if login is successful
        res.redirect('/dashboard');
    } else {
        // Redirect back to login page with an error
        res.redirect('/?error=Invalid credentials');
    }
});

// Serve dashboard page op i am the currebt servers, because of the redirct system in thec fucntion of server
app.get('/dashboard', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'dashboard.html'));
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
