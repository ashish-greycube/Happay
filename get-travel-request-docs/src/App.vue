<template>
  <div class="grid place-content-center pt-10">
    <div class="flex-col w-[35rem] p-2 my-2 shadow-md">
      <p class="text-3xl p-2 text-center">Project Travel Request</p>
      <br>
      <div class="text-center text-red-500"><span class="text-xl italic font-medium">Pending at TA </span> Count (s) : {{ pendingReq.data.length }}</div>
      <br>
      <div>
        <!-- <div class="p-2" :required="true">
          <FormControl
          :type="'text'"
          :ref_for="true"
          size="md"
          variant="subtle"
          placeholder="Project Travel Request Doc"
          :disabled="true"
          label="Project Travel Request Doc"
          v-model="travelReqDoc"
        />
        </div> -->
        <div class="p-2">
          <Link
            v-model="travel.travelDoc"
            doctype="Project Travel Request"
            :label="('Project Travel Request')"
            :required="true"
            :filters="{
              docstatus: 1,
              workflow_state: 'Pending at TA'
            }"
          />
        </div>

        <div class="p-2">
        <FormControl
          :type="'date'"
          :ref_for="true"
          size="md"
          variant="subtle"
          placeholder="Supplier Invoice Date"
          :disabled="false"
          :required="required"
          label="Supplier Invoice Date"
          v-model="invoiceDate"
        />
      </div>

      <div class="p-2">
      <FormControl
        :type="'text'"
        :ref_for="true"
        size="md"
        variant="subtle"
        placeholder="Supplier Invoice Number"
        :disabled="false"
        label="Supplier Invoice Number"
        v-model="invoiceNumber"
        :class="required && 'reqd'"
      />
    </div>

    <div class="p-2">
      <FormControl
      :type="'number'"
      :ref_for="true"
      size="md"
      variant="subtle"
      placeholder="Bill Amount"
      :disabled="false"
      label="Bill Amount"
      :required="true"
      v-model="billAmount"
    />
    </div>

    <div class="p-2">
      <FormControl
      :type="'number'"
      :ref_for="true"
      size="md"
      variant="subtle"
      placeholder="Service Charges"
      :disabled="false"
      label="Service Charges"
      v-model="serviceCharges"
      required
    />
    </div>

    <div class="text-center p-2">
      <ErrorMessage :message="validateCharges" />
    </div>

    <!-- <div class="p-2 text-center" :required="true">
      <FileUploader
            v-if="!travel.ticket_image"
            :fileTypes="['image/*']"
            :validateFile="validateFile"
            @success="(file) => saveTicketImage(file)"
          >
            <template
              v-slot="{ file, progress, uploading, openFileSelector }"
            >
              <div class="mb-4">
                <Button @click="openFileSelector" :loading="uploading">
                  {{
                    uploading ? `Uploading ${progress}%` : 'Upload a Ticket'
                  }}
                </Button>
              </div>
            </template>
      </FileUploader>
      <div v-else class="mb-4">
        <div class="text-xs text-gray-600 mb-1">
          {{ ('Ticket') }}
        </div>
        <div class="flex items-center">
          <div class="border rounded-md p-2 mr-2">
            <FileText class="h-5 w-5 stroke-1.5 text-gray-700" />
          </div>
          <div class="flex flex-col">
            <span>
              {{ travel.ticket_image.file_name }}
            </span>
          </div>
          <X
            @click="removeTicketImage()"
            class="bg-gray-200 rounded-md cursor-pointer stroke-1.5 w-5 h-5 p-1 ml-4"
          />
        </div>
      </div>

      </div> -->

        <div class="p-2 text-center" :required="true">
          <FileUploader
            v-if="!travel.invoice_image"
            :fileTypes="['image/*']"
            :validateFile="validateFile"
            @success="(file) => saveInvoiceImage(file)"
            >
            <template
              v-slot="{ file, progress, uploading, openFileSelector }"
            >
              <div class="mb-4">
                <Button @click="openFileSelector" :loading="uploading">
                  {{
                    uploading ? `Uploading ${progress}%` : 'Upload a Invoice'
                  }}
                </Button>
              </div>
            </template>
          </FileUploader>
          <div v-else class="mb-4">
            <div class="text-xs text-gray-600 mb-1">
              {{ ('Invoice') }}
            </div>
            <div class="flex items-center">
              <div class="border rounded-md p-2 mr-2">
                <FileText class="h-5 w-5 stroke-1.5 text-gray-700" />
              </div>
              <div class="flex flex-col">
                <span>
                  {{ travel.invoice_image.file_name }}
                </span>
                <!-- <span class="text-sm text-gray-500 mt-1">
                  {{ getFileSize(travel.ticket_image.file_size) }}
                </span> -->
              </div>
              <X
                @click="removeInvoiceImage()"
                class="bg-gray-200 rounded-md cursor-pointer stroke-1.5 w-5 h-5 p-1 ml-4"
              />
            </div>
          </div>
        </div>
 
      </div>

      <div class="text-center p-5">
        <Button
          class="p-2"
          :variant="'solid'"
          :ref_for="true"
          theme="gray"
          size="md"
          label="Button"
          :loading="false"
          :loadingText="null"
          :disabled="false"
          v-on:click="updateAmount"
          >
          Send Request
        </Button>

        <!-- <Button @click="dialog1 = true">
          Show Dialog
        </Button>
        <Dialog
          :options="{
            title: 'Confirm',
            message: 'Are you sure you want to confirm this action?',
            size: 'xl',
            icon: {
              name: 'alert-triangle',
              appearance: 'warning',
            },
            actions: [
              {
                label: 'Confirm',
                variant: 'solid',
                onClick: () => {
                              return createPromise();
                            },
              },
            ],
          }"
          v-model="dialog1"
        /> -->
      
        <div class="text-center p-2">
          <ErrorMessage :message="errorMessage" />
        </div>

        <div class="text-center p-2">
          <ErrorMessage :message="throwMessage" />
        </div>
        
      </div>
      
    </div>
  </div>

</template>


<script setup>
import { ref, reactive, inject, onMounted, compile } from 'vue'
import { FileText, X } from 'lucide-vue-next'
import Link from '@/Link.vue'
import {FileUploader, FormControl, createListResource, Dialog, toast, ErrorMessage} from "frappe-ui"
import { useRouter } from 'vue-router'

const url = new URL(window.location.href);
const params = new URLSearchParams(url.search);
let queryParams = Object.fromEntries(params);
let travelDoc = queryParams.name

// const router = useRouter()
// const dialog1 = ref(false)

const __ = inject("$translate")

// const travelReqDoc = ref(travelDoc);
const invoiceDate = ref("");
const invoiceNumber = ref("");
const billAmount = ref("");
const serviceCharges = ref("");
const validateCharges = ref("")
const errorMessage = ref("")
const throwMessage = ref("")

const travel = reactive({
	// ticket_image: null,
  invoice_image: null,
  travelDoc: ""
})

travel.travelDoc = travelDoc

// const saveTicketImage = (file) => {
// 	travel.ticket_image = file
// }

// const removeTicketImage = () => {
// 	travel.ticket_image = null
// }

const saveInvoiceImage = (file) => {
  travel.invoice_image = file
}

const removeInvoiceImage = () => {
  travel.invoice_image = null
}

function validateFile(file) {
  let extn = file.name.split('.').pop().toLowerCase()
  if (!['png', 'jpg', 'jpeg', 'pdf', 'xls', 'xlsx'].includes(extn)) {
    return __('Only Images, Excel and Pdf are allowed')
  }
}

function validate_inputs() {
  console.log(invoiceDate.value, Date.now(), Date.now() < new Date(invoiceDate.value), ' Date.now() < invoiceDate.value')
  console.log(billAmount.value < serviceCharges.value, billAmount.value,  serviceCharges.value, 'billAmount.value < serviceCharges.value')

  if (!travel.travelDoc) {
    errorMessage.value = 'Please select Project Travel Request'
    return false
  }
  // if (!travel.ticket_image?.file_url) {
  //   errorMessage.value = 'Ticket is Required.'
  //   return false
  // }
  if (!travel.invoice_image?.file_url) {
    errorMessage.value = 'Invoice is Required.'
    return false
  }

  if(parseFloat(billAmount.value) < parseFloat(serviceCharges.value)){
    validateCharges.value = 'Service Charge should not be more than Bill Amount.'
    return false
  }

  if(Date.now() < new Date(invoiceDate.value)){
    validateCharges.value =  'Supplier Invoice Date should not be greater than today'
    return false
  }
}

const travelReq = createListResource({
  doctype: 'Project Travel Request',
  fields: ['name','bill_amount', 'service_charge', 'ticket_attachment', 'invoice_attachment', 'supplier_invoice_number', 'supplier_invoice_date'],
})

let pendingReq = createListResource({
  doctype: 'Project Travel Request',
  fields: ['name'],
  filters: {
    workflow_state: ['=', 'Pending at TA']
    },
    pageLength: 99999,
})

onMounted(() => {
  if (pendingReq.data == null) {
    pendingReq.fetch()
  }
})

// function setTicketImage(url) {
//   travelReq.setValue
//   travelReq.setValue.submit({
//     name: travelReqDoc.value,
//     ticket_attachment: url
//   })
// }

// function setInvoiceImage(url) {
//   travelReq.setValue
//   travelReq.setValue.submit({
//     name: travelReqDoc.value,
//     invoice_attachment: url
//   })
// }



function updateAmount() {
  if (validate_inputs() == false) return
  else{
    travelReq.setValue
    travelReq.setValue.submit({
      // id of the record
      name: travel.travelDoc,
      // field value pairs to set
      supplier_invoice_date:invoiceDate.value,
      supplier_invoice_number: invoiceNumber.value,
      bill_amount: billAmount.value,
      service_charge: serviceCharges.value,
      // ticket_attachment: travel.ticket_image?.file_url || '',
      invoice_attachment: travel.invoice_image?.file_url || '',
    },
      {
        onSuccess() {
          // window.open('/success-page')
          window.location.replace('/success-page')
          // router.push({name: "success"})
          // window.open(url, "_self");
          console.log("Successs")
          console.log(travelReq, "======travelReq")
          // toast({
          //   title: "Success",
          //   text: ("Set Data in {0} successfully!"),
          //   icon: "check-circle",
          //   position: "bottom-center",
          //   iconClasses: "text-green-500",
          // })

          invoiceDate.value = "",
          invoiceNumber.value = "",
          travel.travelDoc = "",
          billAmount.value = "",
          serviceCharges.value = "",
          // travel.ticket_image = null,
          travel.invoice_image = null

        },
        onError() {
          console.log("Error!!")
          // router.push({name: "success"})
          // router.replace({ path: '/success-page' })
          // router.push({ name: "success" })
          // window.open('/success-page')
          throwMessage.value = 'Something Went Wrong.'
          // toast({
          //   title: "Error",
          //   text: ("Some Issue to Set Data in {0}, Please try Again!"),
          //   icon: "alert-circle",
          //   position: "bottom-center",
          //   iconClasses: "text-red-500",
          // })
        },
        
      },
      
    )

}
}


</script>
