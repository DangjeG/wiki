class EventEmitter {
    constructor() {
        this.subscribers = {};
    }

    subscribe(event, callback) {
        if (!this.subscribers[event]) {
            this.subscribers[event] = [];
        }
        this.subscribers[event].push(callback);
    }

    unsubscribe(event, callback) {
        if (this.subscribers[event]) {
            this.subscribers[event] = this.subscribers[event].filter((cb) => cb !== callback);
        }
    }

    emit(event, data) {
        if (this.subscribers[event]) {
            this.subscribers[event].forEach((callback) => callback(data));
        }
    }
}