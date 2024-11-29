import { FirestoreRepository } from '../repositories/firestoreRepository';

export const firestoreCommands = {
    create: async <T>(collection: string, data: T) => {
        const repository = new FirestoreRepository<T>();
        return await repository.create(collection, data);
    },
    read: async <T>(collection: string, documentId: string) => {
        const repository = new FirestoreRepository<T>();
        return await repository.read(collection, documentId);
    },
    update: async <T>(collection: string, documentId: string, data: Partial<T>) => {
        const repository = new FirestoreRepository<T>();
        return await repository.update(collection, documentId, data);
    },
    delete: async (collection: string, documentId: string) => {
        const repository = new FirestoreRepository<any>();
        return await repository.delete(collection, documentId);
    },
};