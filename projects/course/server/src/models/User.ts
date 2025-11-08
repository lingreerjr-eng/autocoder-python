import mongoose, { Document, Schema } from 'mongoose';

interface IUser extends Document {
  email: string;
  password: string;
  progress: {
    moduleId: string;
    completedLessons: string[];
  }[];
}

const UserSchema: Schema = new Schema({
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  progress: [
    {
      moduleId: String,
      completedLessons: [String]
    }
  ]
});

export default mongoose.model<IUser>('User', UserSchema);