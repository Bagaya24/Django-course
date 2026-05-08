"use client";
import React, { SubmitEvent, useEffect, useState } from 'react'
import toast from 'react-hot-toast';
import api from '../api/Api';
import { Trash } from 'lucide-react';
import { BarLoader } from 'react-spinners';

export default function HomePage() {
  const [notes, setNotes] = useState<string[]>([]);
  const [title, setTitle] = useState<string>("");
  const [content, setContent] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const getNotes = async () => {
    try {
      const response = await api.get("/notes/");
      setNotes(response.data);
    } catch (error) {
      toast.error("Failed to fetch notes");
      console.error(error);

    }
  };

  const deleteNote = async (id: string) => {
    try {
      const response = await api.delete(`/notes/delete/${id}/`);
      if (response.status === 204) {
        toast.success("Note deleted successfully");
      }

      getNotes();
    } catch (error) {
      toast.error("Failed to delete note");
      console.error(error);
    }
  };

  const createNote = async (e: SubmitEvent<HTMLElement>) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await api.post("/notes/", {
        title,
        content
      });
      if (response.status === 201) {
        toast.success(`Note created`)
        setTitle("");
        setContent("")
        getNotes();
      };

    } catch (error) {
      toast.error("Failed to create note");
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    getNotes();
  }, []);

  return (
    <div className='w-full h-full flex justify-center items-center'>
      <div className='w-8/12 h-8/12 grid grid-cols-5'>

        <div className='col-span-2 flex items-center'>
          <div>
            {notes.map((note: any) => (
              <div className='border border-warning/10 p-2 rounded-2xl mb-1 h-auto' key={note.id}>
              <p className='text-warning/50 text-lg'>{note.title}</p>
              <p className='text-gray-100 text-sm'>{note.content}</p>
              <p>{new Date(note.created_at).toLocaleDateString("fr-FR")}</p>
              <button className='btn btn-sm btn-outline btn-warning' onClick={() => deleteNote(note.id)}><Trash className='w-4 h-4'/></button>
              </div>
            ))}
          </div>
            
          

        </div>
        <div className='col-span-3 flex items-center justify-center '>
          <form onSubmit={createNote} className='w-full'>
            <fieldset className="fieldset bg-base-200 border-base-300 rounded-box w-10/12 border p-4">
              <legend className="fieldset-legend">Create note</legend>

              <label className="label">Title</label>
              <input
                type="text"
                className="input w-full"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Title"
                required />

              <label className='label'>Content</label>
              <textarea
                className="textarea h-24 w-full"
                placeholder="Content"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                required
              ></textarea>
              <button className="btn btn-neutral mt-4" type='submit' disabled={loading}>Create</button>
              {loading && (
                    <div className='w-full flex justify-center'>
                        <BarLoader 
                        color='#e58d47'
                        />
                    </div>
                    
                )}
            </fieldset>
          </form>
        </div>

      </div>
    </div>
  )
}
