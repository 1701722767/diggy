<template>
 <div id="app">
    <v-app>
        <v-dialog v-model="dialog" persistent max-width="600px" min-width="360px">
            <div>
                <v-tabs v-model="tab" show-arrows background-color="deep-purple accent-4" icons-and-text dark grow>
                    <v-tabs-slider color="purple darken-4"></v-tabs-slider>
                    <v-tab v-for="i in tabs" :key="i">
                        <v-icon large>{{ i.icon }}</v-icon>
                        <div class="caption py-1">{{ i.name }}</div>
                    </v-tab>
                    <v-tab-item>
                        <v-card class="px-4"> 
                            <v-card-text>
                                <v-form ref="loginForm" v-model="valid" lazy-validation>
                                    <v-row>
                                        <v-col cols="12">
                                            <v-text-field v-model="loginEmail" :rules="loginEmailRules" label="Correo electrónico" required></v-text-field>
                                        </v-col>
                                        <v-col cols="12">
                                            <v-text-field v-model="loginPassword" :append-icon="show1?'eye':'eye-off'" :rules="[rules.required, rules.min]" :type="show1 ? 'text' : 'password'" name="input-10-1" label="Contraseña" hint="At least 8 characters" counter @click:append="show1 = !show1"></v-text-field>
                                        </v-col>
                                        <v-col class="d-flex" cols="12" sm="6" xsm="12">
                                        </v-col>
                                        <v-spacer></v-spacer>
                                        <v-col class="d-flex" cols="12" sm="3" xsm="12" align-end>
                                            <v-btn x-large block :disabled="!valid" color="success" @click="validate"> Login </v-btn>
                                        </v-col>
                                    </v-row>
                                </v-form>
                            </v-card-text>
                        </v-card>
                    </v-tab-item>
                    <v-tab-item>
                        <v-card class="px-4">
                            <v-card-text>
                                <v-form ref="registerForm" v-model="valid" lazy-validation>
                                    <v-row>
                                        <v-col cols="12" sm="6" md="6">
                                            <v-text-field v-model="firstName"  label="Nombre" maxlength="20" required></v-text-field>
                                        </v-col>
                                        <v-col cols="12" sm="6" md="6">
                                            <v-text-field v-model="lastName"  label="Apellido" maxlength="20" required></v-text-field>
                                        </v-col>
                                        <v-col cols="12">
                                            <v-text-field v-model="username" :rules="[rules.required]" label="Username" required></v-text-field>
                                        </v-col>
                                        <v-col cols="12">
                                            <v-text-field v-model="numberValue" :rules="[rules.required]" type="number" label="Número telefónico" required></v-text-field>
                                        </v-col>
                                        <v-col cols="12">
                                            <v-text-field v-model="email" :rules="emailRules" label="Correo electrónico" required></v-text-field>
                                        </v-col>
                                        <v-col cols="12">
                                           <v-menu
                                                ref="menu"
                                                v-model="menu"
                                                :rules="[rules.required]"
                                                :close-on-content-click="false"
                                                transition="scale-transition"
                                                offset-y
                                                min-width="auto"
                                              >
                                                <template v-slot:activator="{ on, attrs }">
                                                  <v-text-field
                                                    v-model="date"
                                                    label="Fecha de nacimiento"
                                                    prepend-icon="mdi-calendar"
                                                    readonly
                                                    v-bind="attrs"
                                                    v-on="on"
                                                  ></v-text-field>
                                                </template>
                                                <v-date-picker
                                                  v-model="date"
                                                  :active-picker.sync="activePicker"
                                                  :max="
                                                    new Date(
                                                      Date.now() -
                                                        new Date().getTimezoneOffset() * 60000
                                                    )
                                                      .toISOString()
                                                      .substr(0, 10)
                                                  "
                                                  min="1950-01-01"
                                                  @change="save"
                                                ></v-date-picker>
                                              </v-menu>
                                        </v-col>
                                        <v-col cols="12">
                                            <v-text-field v-model="password" :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'" :rules="[rules.required, rules.min]" :type="show1 ? 'text' : 'password'" name="input-10-1" label="Contraseña" hint="At least 8 characters" counter @click:append="show1 = !show1"></v-text-field>
                                        </v-col>
                                        <v-col cols="12">
                                            <v-text-field block v-model="verify" :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'" :rules="[rules.required, passwordMatch]" :type="show1 ? 'text' : 'password'" name="input-10-1" label="Confirme la contraseña" counter @click:append="show1 = !show1"></v-text-field>
                                        </v-col>
                                        <v-spacer></v-spacer>
                                        <v-col class="d-flex ml-auto" cols="12" sm="3" xsm="12">
                                            <v-btn x-large block :disabled="!valid" color="success" @click="validate">Registrar</v-btn>
                                        </v-col>
                                    </v-row>
                                </v-form>
                            </v-card-text>
                        </v-card>
                    </v-tab-item>
                </v-tabs>
            </div>
        </v-dialog>
    </v-app>
</div>
</template>


<script>
  export default {
    name: 'HelloWorld',
    computed: {
    passwordMatch() {
      return () => this.password === this.verify || "Las contraseñas deben coincidir";
    }
  },
  methods: {
    validate() {
      if (this.$refs.loginForm.validate()) {
        // submit form to server/API here...
      }
    },
    reset() {
      this.$refs.form.reset();
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    },
    save (date) {
        this.$refs.menu.save(date)
      },
  },
  data: () => ({
    menu: false,
    dialog: true,
    tab: 0,
    tabs: [
        {name:"Iniciar sesión", icon:"mdi-account"},
        {name:"Registro", icon:"mdi-account-outline"}
    ],
    valid: true,
    
    nombre: "",
    apellido: "",
    username:"",
    telefono:"",
    correo: "",
    fecha_nacimiento:null,
    password: "",
    verify: "",
    loginPassword: "",
    loginEmail: "",
    loginEmailRules: [
      v => !!v || "Campo obligatorio",
      v => /.+@.+\..+/.test(v) || "El correo debe ser valido"
    ],
    emailRules: [
      v => !!v || "Campo obligatorio",
      v => /.+@.+\..+/.test(v) || "El correo debe ser valido"
    ],

    show1: false,
    rules: {
      required: value => !!value || "Campo requerido",
      min: v => (v && v.length >= 8) || "Debe contener al menos 8 caracteres"
    }
  })
  }
</script>
