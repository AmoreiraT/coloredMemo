import { DocumentData, collection, deleteDoc, doc, getDoc, setDoc, updateDoc } from 'firebase/firestore';
import { db } from '../firebase';

export interface IRepository<T> {
    create(collectionName: string, data: T): Promise<T>;
    read(collectionName: string, documentId: string): Promise<T>;
    update(collectionName: string, documentId: string, data: Partial<T>): Promise<T>;
    delete(collectionName: string, documentId: string): Promise<void>;
}

export const createFirestoreRepository = <T extends Record<string, unknown>>(): IRepository<T> => {
    const create = async (collectionName: string, data: T): Promise<T> => {
        const collectionRef = collection(db, collectionName);
        const docRef = doc(collectionRef);
        await setDoc(docRef, data);
        return data;
    };

    const read = async (collectionName: string, documentId: string): Promise<T> => {
        const docRef = doc(db, collectionName, documentId);
        const docSnap = await getDoc(docRef);
        if (docSnap.exists()) {
            return docSnap.data() as T;
        }
        throw new Error('Document not found');
    };

    const update = async (collectionName: string, documentId: string, data: Partial<T>): Promise<T> => {
        const docRef = doc(db, collectionName, documentId);
        await updateDoc(docRef, data as DocumentData);
        const updatedData = { ...data, id: documentId };
        return updatedData as unknown as T;
    };

    const delete_ = async (collectionName: string, documentId: string): Promise<void> => {
        const docRef = doc(db, collectionName, documentId);
        await deleteDoc(docRef);
    };

    return {
        create,
        read,
        update,
        delete: delete_
    };
};