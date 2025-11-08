import mongoose, { Document, Schema } from 'mongoose';

interface ILesson {
  id: string;
  title: string;
  summary: string;
}

interface IModule extends Document {
  id: string;
  title: string;
  description: string;
  duration: string;
  difficulty: string;
  lessons: ILesson[];
}

const ModuleSchema: Schema = new Schema({
  id: { type: String, required: true, unique: true },
  title: { type: String, required: true },
  description: { type: String, required: true },
  duration: { type: String, required: true },
  difficulty: { type: String, required: true },
  lessons: [
    {
      id: String,
      title: String,
      summary: String
    }
  ]
});

export default mongoose.model<IModule>('Module', ModuleSchema);