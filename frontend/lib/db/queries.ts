// lib/db/queries.ts (stubbed version for SchemaSense demo)

export async function getUser(email: string) {
  return []; // no users
}

export async function createUser(email: string, password: string) {
  return { id: "user-dummy", email };
}

export async function createGuestUser() {
  return [{ id: "guest-dummy", email: "guest@example.com" }];
}

export async function saveChat({ id, userId, title, visibility }: any) {
  return { id, userId, title, visibility };
}

export async function deleteChatById({ id }: { id: string }) {
  return { id };
}

export async function deleteAllChatsByUserId({ userId }: { userId: string }) {
  return { deletedCount: 0 };
}

export async function getChatsByUserId() {
  return { chats: [], hasMore: false };
}

export async function getChatById({ id }: { id: string }) {
  return { id, messages: [] };
}

export async function saveMessages({ messages }: { messages: any[] }) {
  return messages;
}

export async function updateMessage({ id, parts }: any) {
  return { id, parts };
}

export async function getMessagesByChatId({ id }: { id: string }) {
  return [];
}

export async function voteMessage({ chatId, messageId, type }: any) {
  return { chatId, messageId, isUpvoted: type === "up" };
}

export async function getVotesByChatId({ id }: { id: string }) {
  return [];
}

export async function saveDocument({ id, title, kind, content, userId }: any) {
  return { id, title, kind, content, userId };
}

export async function updateDocumentContent({ id, content }: any) {
  return { id, content };
}

export async function getDocumentsById({ id }: { id: string }) {
  return [];
}

export async function getDocumentById({ id }: { id: string }) {
  return { id, title: "dummy", content: "" };
}

export async function deleteDocumentsByIdAfterTimestamp({ id, timestamp }: any) {
  return [];
}

export async function saveSuggestions({ suggestions }: { suggestions: any[] }) {
  return suggestions;
}

export async function getSuggestionsByDocumentId({ documentId }: { documentId: string }) {
  return [];
}

export async function getMessageById({ id }: { id: string }) {
  return [];
}

export async function deleteMessagesByChatIdAfterTimestamp({ chatId, timestamp }: any) {
  return [];
}

export async function updateChatVisibilityById({ chatId, visibility }: any) {
  return { chatId, visibility };
}

export async function updateChatTitleById({ chatId, title }: any) {
  return { chatId, title };
}

export async function getMessageCountByUserId({ id, differenceInHours }: any) {
  return 0;
}

export async function createStreamId({ streamId, chatId }: any) {
  return { streamId, chatId };
}

export async function getStreamIdsByChatId({ chatId }: { chatId: string }) {
  return [];
}
