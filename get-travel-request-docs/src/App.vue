<template>
  <div class="grid place-content-center">
    <div class="flex-col w-96 pt-10">
      <p class="text-3xl p-2 text-center">Project Travel Request</p>

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
          :required="true"
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
      />
    </div>

    <div class="p-2">
      <FormControl
      :type="'text'"
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
      :type="'text'"
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

    <div class="p-2 text-center" :required="true">
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
            <!-- <span class="text-sm text-gray-500 mt-1">
              {{ getFileSize(travel.ticket_image.file_size) }}
            </span> -->
          </div>
          <X
            @click="removeTicketImage()"
            class="bg-gray-200 rounded-md cursor-pointer stroke-1.5 w-5 h-5 p-1 ml-4"
          />
        </div>
      </div>

            <!-- <FileUploader
              file-types="image/*"
              @success="(file) => setTicketImage(file.file_url)"
              :validateFile="validateFile"
              v-model="ticketUp">
              <template #default="{ openFileSelector }">
                  <Button @click="openFileSelector">Ticket</Button>
              </template>
            </FileUploader> -->
        </div>

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
      </div>

    </div>
  </div>

</template>


<script setup>
import { ref, reactive, inject } from 'vue'
import { FileText, X } from 'lucide-vue-next'
import Link from '@/Link.vue'
import {Autocomplete, FileUploader, FormControl, createListResource, Dialog, toast} from "frappe-ui"

const url = new URL(window.location.href);
const params = new URLSearchParams(url.search);
let queryParams = Object.fromEntries(params);
let travelDoc = queryParams.name

const __ = inject("$translate")

// const travelReqDoc = ref(travelDoc);
const invoiceDate = ref("");
const invoiceNumber = ref("");
const billAmount = ref("");
const serviceCharges = ref("");

const travel = reactive({
	ticket_image: null,
  invoice_image: null,
  travelDoc: ""
})

travel.travelDoc = travelDoc

const saveTicketImage = (file) => {
	travel.ticket_image = file
}

const removeTicketImage = () => {
	travel.ticket_image = null
}

const saveInvoiceImage = (file) => {
  travel.invoice_image = file
}

const removeInvoiceImage = () => {
  travel.invoice_image = null
}

function validateFile(file) {
  let extn = file.name.split('.').pop().toLowerCase()
  if (!['png', 'jpg', 'jpeg'].includes(extn)) {
    return __('Only PNG and JPG images are allowed')
  }
}

const travelReq = createListResource({
  doctype: 'Project Travel Request',
  fields: ['name','bill_amount', 'service_charge', 'ticket_attachment', 'invoice_attachment', 'supplier_invoice_number', 'supplier_invoice_date'],
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
  travelReq.setValue
  travelReq.setValue.submit({
    // id of the record
    name: travel.travelDoc,
    // field value pairs to set
    supplier_invoice_date:invoiceDate.value,
    supplier_invoice_number: invoiceNumber.value,
    bill_amount: billAmount.value,
    service_charge: serviceCharges.value,
    ticket_attachment: travel.ticket_image?.file_url || '',
    invoice_attachment: travel.invoice_image?.file_url || '',
  },
    {
      onSuccess() {
        // window.open('/success-page')
        window.location.replace('/success-page')
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
      },
      onError() {
        console.log("Error!!")
        // toast({
        //   title: "Error",
        //   text: ("Some Issue to Set Data in {0}, Please try Again!"),
        //   icon: "alert-circle",
        //   position: "bottom-center",
        //   iconClasses: "text-red-500",
        // })
      },
    },

    invoiceDate.value = "",
    invoiceNumber.value = "",
    travel.travelDoc = "",
    billAmount.value = "",
    serviceCharges.value = "",
    travel.ticket_image = null,
    travel.invoice_image = null,
  )
}


</script>
