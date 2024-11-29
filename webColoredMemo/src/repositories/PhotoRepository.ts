// src/repositories/PhotoRepository.ts
import { addDoc, collection, deleteDoc, doc, getDocs, query, updateDoc, where } from 'firebase/firestore';
import { db } from '../firebase';
import { Photo } from '../types/Photo';

class PhotoRepository {
    private collectionName = 'photos';

    async getAll(): Promise<Photo[]> {
        const snapshot = await getDocs(collection(db, this.collectionName));
        return snapshot.docs.map(doc => ({
            id: doc.id,
            ...doc.data()
        })) as Photo[];
    }

    async getByStatus(status: Photo['status']): Promise<Photo[]> {
        const q = query(
            collection(db, this.collectionName),
            where('status', '==', status)
        );
        const snapshot = await getDocs(q);
        return snapshot.docs.map(doc => ({
            id: doc.id,
            ...doc.data()
        })) as Photo[];
    }

    async add(photo: Omit<Photo, 'id'>): Promise<string> {
        const docRef = await addDoc(collection(db, this.collectionName), {
            ...photo,
            status: 'pending'
        });
        return docRef.id;
    }

    async update(id: string, data: Partial<Photo>): Promise<void> {
        const docRef = doc(db, this.collectionName, id);
        await updateDoc(docRef, data);
    }

    async delete(id: string): Promise<void> {
        await deleteDoc(doc(db, this.collectionName, id));
    }
}


export { PhotoRepository };
export type { Photo };

