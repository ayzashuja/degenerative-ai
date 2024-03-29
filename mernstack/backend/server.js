import express from "express";
import cors from "cors";
import mongoose from "mongoose";
import dotenv from 'dotenv';
import User from "./models/user.model.js";

dotenv.config();

const app = express();

const port = 5000;

app.use(cors());
app.use(express.json());

const uri = process.env.ATLAS_URI;
mongoose.connect(uri, { useNewUrlParser: true }); //, useCreateIndex: true });
const connection = mongoose.connection;
connection.once('open', () => {
    console.log("MongoDB database connection established successfully");
})

app.post('/', async (req, res) => {
    const { username, password } = req.body;
    const user = await User.findOne({ username: username });
    if (!user) {
      res.status(401).json({ error: 'Invalid username or password' });
      return;
    }
    if (password !== user.password) {
      res.status(401).json({ error: 'Invalid username or password' });
      return;
    }
    res.json({ message: 'Login successful' });
});

app.post('/signup', async (req, res) => {
    const { username, password } = req.body;
    const wins = 0;
    const totalpoints = 0;
  
    // Check if username is already taken
    const existingUser = await User.findOne({ username });
    if (existingUser) {
      return res.status(409).json({ error: 'Username is already taken' });
    }
  
    // Validate password
    const passwordRegex = /^(?=.*[A-Z])(?=.*[0-9]).{8,}$/;
    if (!passwordRegex.test(password)) {
      return res.status(400).json({ error: 'Password must be at least 8 characters long and contain at least one uppercase letter and one number' });
    }
  
    // Create new user
    const newUser = new User({ username, password, wins, totalpoints });
    await newUser.save();
    
    res.status(201).json({ message: 'User created successfully' });
});

app.listen(port, () => {
    console.log(`Server is running on port: ${port}`);
});