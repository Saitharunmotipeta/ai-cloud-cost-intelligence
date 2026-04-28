import { ApolloClient, InMemoryCache, HttpLink } from "@apollo/client";
import { setContext } from "@apollo/client/link/context";

const authLink = setContext((_, { headers }) => {
  const accountId = localStorage.getItem("account_id");

  return {
    headers: {
      ...headers,
      "X-Account-ID": accountId || "",
    },
  };
});

const client = new ApolloClient({
  link: authLink.concat(new HttpLink({ uri: "http://13.50.112.87:8000/graphql" })),
  cache: new InMemoryCache(),
});

export default client;