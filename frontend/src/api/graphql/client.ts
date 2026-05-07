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
  // link: authLink.concat(new HttpLink({ uri: "https://4vycd1l8uj.execute-api.eu-north-1.amazonaws.com/prod/graphql" })),
  link: authLink.concat(new HttpLink({ uri: "https:localhost:8000/graphql" })),
  cache: new InMemoryCache(),
});

export default client;