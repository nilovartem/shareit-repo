<template>
    <h1>This is page</h1>
    <br/>
    <div>
        <table>
            <thead>Список ссылок</thead>
            <tr v-for="row in links">
                <td>{{ row['id'] }}</td>
                <td>{{ row['url'] }}</td>
            </tr>
        </table>
    </div>
    
</template>
<script>
import axios from 'axios';
export default {
    data(){
        return{
            links:null
        }
    },
    props: ['url'],
    methods: {
        async getLinksForPage(url){
            const path = "http://127.0.0.1:5000/shareit/api/v1.0/links/view/" + url
            let data = []
            try{
                const response = await axios.get(path)
                console.log(response.status)
                data = response.data
            }
            catch (error){
                console.error(error)
            }            
            return data
        }
    },
    created(){
        this.getLinksForPage(this.url).then(data => {
            let test = data[0]
            console.log(test)
            console.log(test['page_url'])
            this.links = data
        })
        //console.log(data)
        
    }
}

//get data from db
</script>