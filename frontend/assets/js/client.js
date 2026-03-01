(function attachMoodSwingsClient(globalScope) {
  const defaultBaseURL = "http://127.0.0.1:8000";

  function createClient(options = {}) {
    if (!globalScope.axios) {
      throw new Error("Axios is required. Please include axios before client.js");
    }

    const instance = globalScope.axios.create({
      baseURL: options.baseURL || defaultBaseURL,
      timeout: options.timeout || 10000,
    });

    return {
      createUser() {
        return instance.post("/users").then((response) => response.data);
      },

      createMoods(userId, moods) {
        return instance
          .post("/moods", { moods }, { params: { user_id: userId } })
          .then((response) => response.data);
      },

      getTodaysMoods(userId) {
        return instance
          .get("/moods/today", { params: { user_id: userId } })
          .then((response) => response.data);
      },

      updateTodaysMoods(userId, moods) {
        return instance
          .put("/moods/today", { moods }, { params: { user_id: userId } })
          .then((response) => response.data);
      },

      createNote(userId, note) {
        return instance
          .post("/notes", { note }, { params: { user_id: userId } })
          .then((response) => response.data);
      },

      getLatestNotes(options = {}) {
        const params = {
          limit: options.limit ?? 5,
          offset: options.offset ?? 0,
        };

        return instance
          .get("/notes/latest", { params })
          .then((response) => response.data);
      },

      getMoodFrequency() {
        return instance.get("/mood-frequency").then((response) => response.data);
      },

      getWeeklyTrend() {
        return instance.get("/weekly-trend").then((response) => response.data);
      },

      getTopHappyWords() {
        return instance.get("/top-happy-words").then((response) => response.data);
      },

      getUserHistory(userId) {
        return instance
          .get("/user-history", { params: { user_id: userId } })
          .then((response) => response.data);
      },
    };
  }

  globalScope.MoodSwingsClient = {
    createClient,
  };
})(window);