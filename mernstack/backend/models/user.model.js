import mongoose from "mongoose";
import uniqueValidator from "mongoose-unique-validator";

const Schema = mongoose.Schema;

// const userSchema = new Schema({
//     username: {
//         type: String,
//         required: true,
//         unique: true,
//         trim: true,
//         minlength: 3,
//         maxlength: 20,
//         validate: {
//             validator: function(v) {
//               return /^[a-zA-Z0-9]+$/.test(v);
//             },
//             message: props => `${props.value} is not a valid username!`
//         }
//     },
//     password: {
//         type: String,
//         required: true,
//         minlength: 8,
//         validate: {
//             validator: function(v) {
//                 return /^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$/.test(v);
//             },
//         message: props => `${props.value} is not a valid password!`
//         }
//     }
// });

// userSchema.plugin(uniqueValidator);

// const User = mongoose.model('User', userSchema);


const userSchema = new mongoose.Schema({
    username: { type: String, required: true, unique: true },
    password: { type: String, required: true },
    wins: { type: Number},
    totalpoints: { type: Number},
});
  
const User = mongoose.model('User', userSchema);
  




export default User;