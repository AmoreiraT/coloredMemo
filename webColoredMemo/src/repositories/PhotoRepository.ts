// src/repositories/photoRepository.ts
import { addDoc, collection, deleteDoc, doc, getDocs, query, updateDoc, where } from 'firebase/firestore';
import { db } from '../firebase';
import { Photo } from '../types/Photo';

const createPhotoRepository = () => {
    const collectionName = 'photos';

    const getAll = async (): Promise<Photo[]> => {
        const snapshot = await getDocs(collection(db, collectionName));
        return snapshot.docs.map(doc => ({
            id: doc.id,
            ...doc.data()
        })) as Photo[];
    };

    const getByStatus = async (status: Photo['status']): Promise<Photo[]> => {
        const q = query(
            collection(db, collectionName),
            where('status', '==', status)
        );
        const snapshot = await getDocs(q);
        return snapshot.docs.map(doc => ({
            id: doc.id,
            ...doc.data()
        })) as Photo[];
    };

    const add = async (photo: Omit<Photo, 'id'>): Promise<string> => {
        const docRef = await addDoc(collection(db, collectionName), {
            ...photo,
            status: 'pending'
        });
        return docRef.id;
    };

    const update = async (id: string, data: Partial<Photo>): Promise<void> => {
        const docRef = doc(db, collectionName, id);
        await updateDoc(docRef, data);
    };

    const delete_ = async (id: string): Promise<void> => {
        await deleteDoc(doc(db, collectionName, id));
    };

    return {
        getAll,
        getByStatus,
        add,
        update,
        delete: delete_
    };
};

export { createPhotoRepository };
export type { Photo };

