// src/dataStore.js
import { db } from "./firebase";
import { collection, addDoc, getDocs } from "firebase/firestore";
import { deleteDoc, query, where, doc } from "firebase/firestore";
// Collections
const eventsCollection = collection(db, "events");
const messagesCollection = collection(db, "messages");

// Add event to Firestore
export async function addEvent(event) {
  try {
    //const docRef = await addDoc(eventsCollection, event);
    await addDoc(eventsCollection, event);
    //console.log("Event added with ID:", docRef.id);
  } catch (e) {
    console.error("Error adding event:", e);
  }
}

// Add contact message to Firestore
export async function addMessage(message) {
  try {
    //const docRef = await addDoc(messagesCollection, message);
    await addDoc(messagesCollection, message);
    //console.log("Message added with ID:", docRef.id);
  } catch (e) {
    console.error("Error adding message:", e);
  }
}

// Optional: Get all messages
export async function getAllMessages() {
  try {
    const snapshot = await getDocs(eventsCollection);
    return snapshot.docs.map((doc) => ({ id: doc.id, ...doc.data() }));
  } catch (e) {
    console.error("Error fetching messages:", e);
    return [];
  }
}

const approvedEventsCollection = collection(db, "approved events");

export async function getApprovedEvents() {
  try {
    const snapshot = await getDocs(approvedEventsCollection);
    return snapshot.docs.map((doc) => ({ id: doc.id, ...doc.data() }));
  } catch (e) {
    console.error("Error fetching approved events:", e);
    return [];
  }
}

export async function addApprovedEvent(event) {
  try {
    //const docRef = await addDoc(approvedEventsCollection, event);
    await addDoc(approvedEventsCollection, event);
    //console.log("Approved event added with ID:", docRef.id);
  } catch (e) {
    console.error("Error adding approved event:", e);
  }
}

export async function deleteApprovedEventByName(eventName) {
  const q = query(collection(db, "approved events"), where("eventName", "==", eventName));
  const snapshot = await getDocs(q);


  for (const docSnap of snapshot.docs) {
    await deleteDoc(doc(db, "approved events", docSnap.id));
  }
}