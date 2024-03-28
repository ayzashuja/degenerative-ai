import mongoose from "mongoose";

// const Schema = mongoose.Schema;

// const statsSchema = new Schema({
//     username: { type: String, require: true },
//     wins: { type: Number},
//     totalpoints: { type: Number }
// });

// const Stats = mongoose.model('Stats', statsSchema);

// export default Stats;

const statsSchema = new mongoose.Schema({
    username: String,
    wins: Number,
    totalpoints: Number
});
const Stats = mongoose.model('Stats', statsSchema);
export default Stats;