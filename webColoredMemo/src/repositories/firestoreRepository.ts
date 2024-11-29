import { db } from '../firebase';
import { collection, doc, setDoc, getDoc, updateDoc, deleteDoc } from 'firebase/firestore';
import axios from 'axios';

export interface IRepository<T> {
    create(collectionName: string, data: T): Promise<T>;
    read(collectionName: string, documentId: string): Promise<T>;
    update(collectionName: string, documentId: string, data: Partial<T>): Promise<T>;
    delete(collectionName: string, documentId: string): Promise<void>;
}

export class FirestoreRepository<T> implements IRepository<T> {
    async create(collectionName: string, data: T): Promise<T> {
        const collectionRef = collection(db, collectionName);
        const docRef = doc(collectionRef);
        await setDoc(docRef, data);
        return data;
    }

    async read(collectionName: string, documentId: string): Promise<T> {
        const docRef = doc(db, collectionName, documentId);
        const docSnap = await getDoc(docRef);
        if (docSnap.exists()) {
            return docSnap.data() as T;
        } else {
            throw new Error('Document not found');
        }
    }

    async update(collectionName: string, documentId: string, data: Partial<T>): Promise<T> {
        const docRef = doc(db, collectionName, documentId);
        await updateDoc(docRef, data);
        return { ...data, id: documentId } as T;
    }

    async delete(collectionName: string, documentId: string): Promise<void> {
        const docRef = doc(db, collectionName, documentId);
        await deleteDoc(docRef);
    }
}