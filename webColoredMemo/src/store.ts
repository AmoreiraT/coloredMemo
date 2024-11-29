import {create} from 'zustand';

interface FirestoreState<T> {
    documents: T[];
    addDocument: (doc: T) => void;
    removeDocument: (id: string) => void;
}

export const useFirestoreStore = <T>() => create<FirestoreState<T>>((set) => ({
    documents: [],
    addDocument: (doc) => set((state) => ({ documents: [...state.documents, doc] })),
    removeDocument: (id) => set((state) => ({ documents: state.documents.filter(doc => doc.id !== id) })),
}));