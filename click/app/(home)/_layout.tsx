import { AntDesign, MaterialIcons, FontAwesome, Ionicons } from "@expo/vector-icons";
import { Tabs } from "expo-router";

const HomeRootLayout = () => {
  return (
    <Tabs screenOptions={{
        tabBarActiveTintColor: '#575757',
        headerShown: false
    }} >
      <Tabs.Screen name="index" options={{
        title: 'Feed',
        headerShown: true,
        tabBarIcon: ({ color }) => <AntDesign name="home" size={24} color={color} />,
      }} />
      <Tabs.Screen name="info" options={{
        title: 'Notifications',
        headerShown: true,
        tabBarIcon: ({ color }) => <MaterialIcons name="notifications" size={24} color={color} />,
      }} />
        <Tabs.Screen name="profile" options={{
        title: 'Profile',
        headerShown: true,
        tabBarIcon: ({ color }) => <FontAwesome name="user-o" size={24} color={color} />
      }} />
       <Tabs.Screen name="post" options={{
        title: 'Post',
        headerShown: true,
        tabBarIcon: ({ color }) => <MaterialIcons name="add" size={24} color={color} />
       }} />
    </Tabs>
  )
}

export default HomeRootLayout;